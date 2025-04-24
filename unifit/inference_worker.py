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

MODEL_DIR = "/mnt/efs/manickavela/unifit/unifit_models"

@serve.deployment(
    name="static_unifit",
    ray_actor_options={"num_cpus": 0.2, 
                       "num_gpus" :0.1})
class UnifitInference:
    def __init__(self):
        self.model_path = "/mnt/efs/manickavela/unifit/unifit_models"
    
    @serve.multiplexed(max_num_models_per_replica=3)
    async def get_model_runtime(self, model_id) -> UniFitRuntime:
        """ Load the model """
        print(f"Loading model {model_id} in path {self.model_path}/{model_id}")
        if not os.path.exists(self.model_path+"/"+model_id):
            raise FileNotFoundError(f"Model path {self.model_path}/{model_id} does not exist")
        try:
            print("Reading UnifitRuntime")
            runtime = UniFitRuntime.initialize_runtime(
                self.model_path+"/"+model_id)
            print("UnifitRuntime initialized")
        except Exception as e:
            print(f"Error initializing UniFitRuntime: {e}")
            raise e
        return runtime

    async def __call__(self, request):
        model_id = serve.get_multiplexed_model_id()
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
        turns = [Turn(speaker=speaker, text=text)]
        runtime: UniFitRuntime = await self.get_model_runtime(model_id)
        # self.infer_runtime([Turn(speaker=speaker, text=text)])
        setting: Settings = runtime.SETTING
        if setting == Settings.SETFIT_WITH_KEYWORDS_BASED_DATA_EXTENSION_AND_SELF_LEARNING:
            turns_speaker_and_text_tuples_list: List[Tuple[str, str]] = [
                (turn.speaker.value, turn.text) for turn in turns
            ]
            outputs: List[RuntimeOutput] = runtime.infer(turns_speaker_and_text_tuples_list)
        else :
            raise NotImplementedError(f"Infering the runtime for setting \"{setting.value}\" is not currently supported")

        return {"message": "Inference completed "+outputs[0].__str__()}

    # def infer_runtime(self, turns: List[Turn]) -> List[str]:
    #     """ Infer runtime on turns """
    #     return outputs

unifit_inference = UnifitInference.bind()
# app1 = "unifit_inference_worker"
# serve.run(target=unifit_inference, name=app1, route_prefix=f"/{app1}")