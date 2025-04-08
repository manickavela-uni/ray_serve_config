import ray
from ray import serve
from typing import List
from starlette.requests import Request

from gliner import GLiNER
import torch
from fastapi import FastAPI

@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 0.5})
class GlinerDeployment:
    # FastAPI will automatically parse the HTTP request for us.
    def __init__(self):
        self.model = GLiNER.from_pretrained("urchade/gliner_medium").to("cuda:0")
        self.model.eval()
        self.sample_text = """
            Libretto by Marius Petipa, based on the 1822 novella ``Trilby, ou Le Lutin d'Argail`` by Charles Nodier, first presented by the Ballet of the Moscow Imperial Bolshoi Theatre on January 25/February 6 (Julian/Gregorian calendar dates), 1870, in Moscow with Polina Karpakova as Trilby and Ludiia Geiten as Miranda and restaged by Petipa for the Imperial Ballet at the Imperial Bolshoi Kamenny Theatre on January 17–29, 1871 in St. Petersburg with Adèle Grantzow as Trilby and Lev Ivanov as Count Leopold.
        """
        self.labels = ["person", "book", "location", "date", "actor", "character"]

    def gliner_predict(self, text: str, labels: List[str], ):
        entities = self.model.predict_entities(text, labels, threshold=0.4)
        return entities

    async def __call__(self, http_request: Request):
        """Handle HTTP requests."""
        # Parse the request body
        data = await http_request.json()
        if isinstance(data, dict):
            text, labels = data.get("text", ""), data.get("labels", [])
        else :
            return {"error": "Invalid request format"}
        
        
        if not text:
            return {"error": "No text provided"}
        if not labels:
            return {"error": "No labels provided"}

        if text == "sample":
            print("Using sample text")
            text = self.sample_text
            labels = self.labels

        # Call the gliner method
        summary = self.gliner_predict(text, labels)
        return {"gliner output": summary}

deployment = GlinerDeployment.bind()
