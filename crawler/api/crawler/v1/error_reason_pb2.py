# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/crawler/v1/error_reason.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pykit.errors import errors_pb2 as pykit_dot_errors_dot_errors__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!api/crawler/v1/error_reason.proto\x12\x0e\x61pi.crawler.v1\x1a\x19pykit/errors/errors.proto*H\n\x0b\x45rrorReason\x12\x19\n\x0fSTOCK_NOT_FOUND\x10\x00\x1a\x04\xa8\x45\x94\x03\x12\x18\n\x0eNODE_NOT_FOUND\x10\x01\x1a\x04\xa8\x45\xf4\x03\x1a\x04\xa0\x45\xf4\x03\x42\x36\n\ncrawler.v1P\x01Z\x19gostock/api.crawler.v1;v1\xa2\x02\nAPIStockV1b\x06proto3')

_ERRORREASON = DESCRIPTOR.enum_types_by_name['ErrorReason']
ErrorReason = enum_type_wrapper.EnumTypeWrapper(_ERRORREASON)
STOCK_NOT_FOUND = 0
NODE_NOT_FOUND = 1


if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\ncrawler.v1P\001Z\031gostock/api.crawler.v1;v1\242\002\nAPIStockV1'
  _ERRORREASON._options = None
  _ERRORREASON._serialized_options = b'\240E\364\003'
  _ERRORREASON.values_by_name["STOCK_NOT_FOUND"]._options = None
  _ERRORREASON.values_by_name["STOCK_NOT_FOUND"]._serialized_options = b'\250E\224\003'
  _ERRORREASON.values_by_name["NODE_NOT_FOUND"]._options = None
  _ERRORREASON.values_by_name["NODE_NOT_FOUND"]._serialized_options = b'\250E\364\003'
  _ERRORREASON._serialized_start=80
  _ERRORREASON._serialized_end=152
# @@protoc_insertion_point(module_scope)
