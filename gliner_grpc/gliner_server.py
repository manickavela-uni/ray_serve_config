from gliner_protos_pb2 import (
    TextsLabels,
    Entity,
    EntityList,
    EntityLists
)
import time
from ray import serve
from gliner import GLiNER
from typing import List
import torch

@serve.deployment(
    num_replicas=2,
    ray_actor_options={"num_cpus": 0.2, "num_gpus" :0.1},
    max_ongoing_requests=100)
class GlinerDeployment:
    def __init__(self):
        self.model = GLiNER.from_pretrained("urchade/gliner_medium")
        self.model.eval()
        if torch.cuda.is_available():
            self.model.to("cuda:0")
        self.sample_text = '''
            Libretto by Marius Petipa, based on the 1822 novella ``Trilby, ou Le Lutin d'Argail`` by Charles Nodier, first presented by the Ballet of the Moscow Imperial Bolshoi Theatre on January 25/February 6 (Julian/Gregorian calendar dates), 1870, in Moscow with Polina Karpakova as Trilby and Ludiia Geiten as Miranda and restaged by Petipa for the Imperial Ballet at the Imperial Bolshoi Kamenny Theatre on January 17–29, 1871 in St. Petersburg with Adèle Grantzow as Trilby and Lev Ivanov as Count Leopold.
        '''
        self.labels = ["person", "book", "location", "date", "actor", "character"]

    def from_entity_to_pb(self, entity: dict) -> Entity:
        pb_entity = Entity()
        pb_entity.start = entity.get('start', 0)   # Defaulting to 0 or any sentinel value
        pb_entity.end = entity.get('end', 0)
        pb_entity.text = entity.get('text', "")
        pb_entity.label = entity.get('label', "")
        pb_entity.score = entity.get('score', 0.0)
        return pb_entity

    def from_entity_lists_to_pb(self, entity_lists: List[List[dict]]) -> EntityLists:
        pb_entity_lists = EntityLists()
        for entity_list in entity_lists:
            pb_entity_list = pb_entity_lists.content.add()
            for entity in entity_list:
                pb_entity = self.from_entity_to_pb(entity)
                pb_entity_list.content.append(pb_entity)
        return pb_entity_lists

    def infer(self, request: TextsLabels) -> EntityList:
        texts, labels, threshold = request.texts, request.labels, request.threshold
        start = time.time()
        entity_lists = self.model.batch_predict_entities(texts=texts, labels=labels, threshold=threshold)
        print(f"time take : {time.time() - start}")
        return self.from_entity_lists_to_pb(entity_lists=entity_lists)

g = GlinerDeployment.bind()
app1 = "gliner"
serve.run(target=g, name=app1, route_prefix=f"/{app1}")