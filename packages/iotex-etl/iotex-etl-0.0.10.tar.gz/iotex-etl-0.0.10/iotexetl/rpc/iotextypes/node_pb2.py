# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/types/node.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/types/node.proto',
  package='iotextypes',
  syntax='proto3',
  serialized_options=b'\n\"com.github.iotexproject.grpc.typesP\001Z5github.com/iotexproject/iotex-proto/golang/iotextypes',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16proto/types/node.proto\x12\niotextypes\"v\n\nServerMeta\x12\x16\n\x0epackageVersion\x18\x01 \x01(\t\x12\x17\n\x0fpackageCommitID\x18\x02 \x01(\t\x12\x11\n\tgitStatus\x18\x03 \x01(\t\x12\x11\n\tgoVersion\x18\x04 \x01(\t\x12\x11\n\tbuildTime\x18\x05 \x01(\tB]\n\"com.github.iotexproject.grpc.typesP\x01Z5github.com/iotexproject/iotex-proto/golang/iotextypesb\x06proto3'
)




_SERVERMETA = _descriptor.Descriptor(
  name='ServerMeta',
  full_name='iotextypes.ServerMeta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='packageVersion', full_name='iotextypes.ServerMeta.packageVersion', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='packageCommitID', full_name='iotextypes.ServerMeta.packageCommitID', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gitStatus', full_name='iotextypes.ServerMeta.gitStatus', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='goVersion', full_name='iotextypes.ServerMeta.goVersion', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='buildTime', full_name='iotextypes.ServerMeta.buildTime', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=156,
)

DESCRIPTOR.message_types_by_name['ServerMeta'] = _SERVERMETA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ServerMeta = _reflection.GeneratedProtocolMessageType('ServerMeta', (_message.Message,), {
  'DESCRIPTOR' : _SERVERMETA,
  '__module__' : 'proto.types.node_pb2'
  # @@protoc_insertion_point(class_scope:iotextypes.ServerMeta)
  })
_sym_db.RegisterMessage(ServerMeta)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
