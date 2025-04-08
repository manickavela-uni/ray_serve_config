import ray
from ray import serve
from typing import List
from starlette.requests import Request

from gliner import GLiNER
import torch
from fastapi import FastAPI

@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 0.2, "num_gpus": 0})
class GlinerDeployment:
    # FastAPI will automatically parse the HTTP request for us.
    def __init__(self):
        self.model = GLiNER.from_pretrained("urchade/gliner_medium")
        self.model.eval()

    def gliner_predict(self, text: str, labels: List[str], ):
        entities = self.model.predict_entities(text, labels, threshold=0.4)
        return entities

    async def __call__(self, http_request: Request):
        """Handle HTTP requests."""
        # Parse the request body
        data = await http_request.json()
        text = data.get("text", "")
        if not text:
            return {"error": "No text provided"}
        text = """
            Libretto by Marius Petipa, based on the 1822 novella ``Trilby, ou Le Lutin d'Argail`` by Charles Nodier, first presented by the Ballet of the Moscow Imperial Bolshoi Theatre on January 25/February 6 (Julian/Gregorian calendar dates), 1870, in Moscow with Polina Karpakova as Trilby and Ludiia Geiten as Miranda and restaged by Petipa for the Imperial Ballet at the Imperial Bolshoi Kamenny Theatre on January 17–29, 1871 in St. Petersburg with Adèle Grantzow as Trilby and Lev Ivanov as Count Leopold.
        """
        labels = ["person", "book", "location", "date", "actor", "character"]
        # Call the gliner method
        summary = self.gliner_predict(text, labels)
        return {"gliner output": summary}

deployment = GlinerDeployment.bind()
