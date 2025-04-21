import time, os
from ray import serve
from typing import List, Tuple
from dataclasses import dataclass
from pydantic import BaseModel
from enum import Enum
import torch
from unifit import UniFitRuntime
from unifit.project.settings import Settings
from unifit.project.unifit_setfit_with_keywords_based_data_extension_and_self_learning_project.unifit_setfit_with_keywords_based_data_extension_and_self_learning_runtime import UniFitSetFitWithKeywordsDataExtensionSelfLearningRuntimeOutput as RuntimeOutput
from fastapi import FastAPI

app = FastAPI()

class Speaker(Enum):
    AGENT = 'agent'
    CUSTOMER = 'customer'
    OTHERS = 'others'
    @classmethod
    def from_string(self, speaker_str) -> 'Speaker':
        if speaker_str.lower() == 'agent':
            return Speaker.AGENT
        elif speaker_str.lower() == 'customer':
            return Speaker.CUSTOMER
        else:
            return Speaker.OTHERS

class Turn(BaseModel):
    speaker: Speaker
    text: str

@serve.deployment(
    num_replicas=1,
    ray_actor_options={"num_cpus": 0.2, "num_gpus" :0.1},
    max_ongoing_requests=100)
class UnifitInference:
    def __init__(self):
        print([os.listdir('/mnt/efs/manickavela/nlp/')])
        model_path = "/mnt/efs/manickavela/nlp/mukesh_model"
        try:
            print("Reading UnifitRuntime")
            self.runtime = UniFitRuntime.initialize_runtime(
                model_path)
            print("UnifitRuntime initialized")
        except Exception as e:
            print(f"Error initializing UniFitRuntime: {e}")
            raise e
                # access FastAPI app object from Serve
    async def __call__(self, request):
        data = await request.json()
        if isinstance(data, dict):
            text = data.get("text", "")
            speaker = data.get("speaker", "others")
        else:
            return {"error": "Invalid request format"}
        if not text:
            return {"error": "No text provided"}
        if not speaker:
            return {"error": "No speaker provided"}
        speaker = Speaker.from_string(speaker)
        self.infer_runtime([Turn(speaker=speaker, text=text)])
        return {"message": "Inference completed"}
        
    def infer_runtime(self, turns: List[Turn]) -> List[str]:
        """ Infer runtime on turns """
        setting: Settings = self.runtime.SETTING
        if setting == Settings.SETFIT_WITH_KEYWORDS_BASED_DATA_EXTENSION_AND_SELF_LEARNING:
            turns_speaker_and_text_tuples_list: List[Tuple[str, str]] = [
                (turn.speaker.value, turn.text) for turn in turns
            ]
            outputs: List[RuntimeOutput] = self.runtime.infer(turns_speaker_and_text_tuples_list)
        else :
            raise NotImplementedError(f"Infering the runtime for setting \"{setting.value}\" is not currently supported")
        return outputs

unifit_inference = UnifitInference.bind()
# app1 = "unifit_inference_worker"
# serve.run(target=unifit_inference, name=app1, route_prefix=f"/{app1}")