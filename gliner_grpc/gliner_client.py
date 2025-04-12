from gliner_protos_pb2 import (
    TextsLabels,
    Entity,
    EntityList,
    EntityLists
)
import gliner_protos_pb2_grpc
from typing import List
import grpc

# def from_pb_to_entity(pb_entity: Entity) -> dict:
#     return {
#         'start': getattr(pb_entity, 'start', 0),       # Always set, defaults to 0
#         'end': getattr(pb_entity, 'end', 0),
#         'text': getattr(pb_entity, 'text', ""),
#         'label': getattr(pb_entity, 'label', ""),
#         'score': getattr(pb_entity, 'score', 0.0)
#     }

# def from_pb_to_entity_lists(pb_entity_lists: EntityLists) -> List[List[dict]]:
#     entity_lists = []
#     # the condition for outer loop is logically incorrect but the logical fallacy is part
#     # of the gRPC library
#     # print("Entity lists ",pb_entity_lists[0].content)
#     for pb_entity_list in pb_entity_lists.content:
#         print("pb_entity_list ", pb_entity_list)
#         entity_list = []
#         for pb_entity in pb_entity_list.content:
#             print('----------------------')
#             print("pb_entity ", pb_entity)
#             entity = from_pb_to_entity(pb_entity)
#             entity_list.append(entity)
#         entity_lists.append(entity_list)
#     return entity_lists


def from_pb_to_entity(pb_entity: Entity) -> dict:
    return {
        "start": pb_entity.start if hasattr(pb_entity, 'start') else 0,
        "end": pb_entity.end if hasattr(pb_entity, 'end') else 0,
        "text": pb_entity.text,
        "label": pb_entity.label,
        "score": pb_entity.score,
    }

def from_pb_to_entity_list(pb_entity_list: EntityList) -> List[dict]:
    return [from_pb_to_entity(pb_entity) for pb_entity in pb_entity_list.content]

def from_pb_to_entity_lists(pb_entity_lists: EntityLists) -> List[List[dict]]:
    return [from_pb_to_entity_list(pb_entity_list) for pb_entity_list in pb_entity_lists.content]

# def run():

texts, labels, threshold = (['agent: hi thanks for calling voya, customer: hi, agent: this is john how can i help you, customer: hi john this is maria, agent: hi maria, customer: i am looking for my claim received date, agent: sure your claim received date is twenty four january twenty twenty four'], ['name of the agent', 'customer phone number', 'account top up amount', 'mobile number', 'customer preferred callback date', 'customer best call back number', 'customer suitable time to connect', 'connect back time', 'best call back date', 'customer preferred call back date', 'sim card number', 'customer payment zip code', 'wireless phone number', 'customer available date', 'number in the sim card', 'customer available time', 'agent reference name', 'agent name', 'connect back date', 'alternate phone number', 'customers calling number', 'call back time', 'additional number to contact', 'customer alternate number', 'record name', 'agent identification name', 'address zip code', 'customer validation name', 'alternate best callback number', 'customer best alternate call back number', 'customer preferred call back time', 'insurance number', 'customer number', 'zip code', 'customer zip code', 'customer name', 'best call back time', 'call back date', 'assurance number', 'new sim card number', 'amount to add', 'name of the customer', 'registered name', 'customer suitable callback time', 'first name', 'current phone number', 'customer suitable date to connect', 'alternate contact number', 'alternate call back number', 'top up amount', 'payment zip code', 'name of the account holder', 'account holder name', 'first and last name', 'name of the customer in record', 'new sim number', 'customer identification name'], 0.1)
with grpc.insecure_channel('localhost:9000') as channel:
    stub = gliner_protos_pb2_grpc.GlinerStub(channel)
    pb_entity_lists = stub.infer(TextsLabels(texts=texts, labels=labels, threshold=threshold))
print(from_pb_to_entity_lists(pb_entity_lists))
    
# if __name__ == "__main__":
#     run()