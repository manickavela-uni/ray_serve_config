# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: gliner_protos.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'gliner_protos.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13gliner_protos.proto\"?\n\x0bTextsLabels\x12\r\n\x05texts\x18\x01 \x03(\t\x12\x0e\n\x06labels\x18\x02 \x03(\t\x12\x11\n\tthreshold\x18\x03 \x01(\x02\"P\n\x06\x45ntity\x12\r\n\x05start\x18\x01 \x01(\x05\x12\x0b\n\x03\x65nd\x18\x02 \x01(\x05\x12\x0c\n\x04text\x18\x03 \x01(\t\x12\r\n\x05label\x18\x04 \x01(\t\x12\r\n\x05score\x18\x05 \x01(\x02\"&\n\nEntityList\x12\x18\n\x07\x63ontent\x18\x01 \x03(\x0b\x32\x07.Entity\"+\n\x0b\x45ntityLists\x12\x1c\n\x07\x63ontent\x18\x01 \x03(\x0b\x32\x0b.EntityList2/\n\x06Gliner\x12%\n\x05infer\x12\x0c.TextsLabels\x1a\x0c.EntityLists\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gliner_protos_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TEXTSLABELS']._serialized_start=23
  _globals['_TEXTSLABELS']._serialized_end=86
  _globals['_ENTITY']._serialized_start=88
  _globals['_ENTITY']._serialized_end=168
  _globals['_ENTITYLIST']._serialized_start=170
  _globals['_ENTITYLIST']._serialized_end=208
  _globals['_ENTITYLISTS']._serialized_start=210
  _globals['_ENTITYLISTS']._serialized_end=253
  _globals['_GLINER']._serialized_start=255
  _globals['_GLINER']._serialized_end=302
# @@protoc_insertion_point(module_scope)
