# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/crawler/v1/stock_info.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from api.crawler.v1 import index_pb2 as api_dot_crawler_dot_v1_dot_index__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x61pi/crawler/v1/stock_info.proto\x12\x0e\x61pi.crawler.v1\x1a\x1cgoogle/api/annotations.proto\x1a\x1a\x61pi/crawler/v1/index.proto\"\xa3\x01\n\x11StockBasicRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05is_hs\x18\x02 \x01(\t\x12\x13\n\x0blist_status\x18\x03 \x01(\t\x12\x10\n\x08\x65xchange\x18\x04 \x01(\t\x12\x0f\n\x07ts_code\x18\x05 \x01(\t\x12\x0e\n\x06market\x18\x06 \x01(\t\x12\r\n\x05limit\x18\x07 \x01(\x05\x12\x0e\n\x06offset\x18\t \x01(\x05\x12\x0c\n\x04name\x18\n \x01(\t\"\x9b\x02\n\nStockBasic\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0f\n\x07ts_code\x18\x02 \x01(\t\x12\x0e\n\x06symbol\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x0c\n\x04\x61rea\x18\x05 \x01(\t\x12\x10\n\x08industry\x18\x06 \x01(\t\x12\x10\n\x08\x66ullname\x18\x07 \x01(\t\x12\x0e\n\x06\x65nname\x18\x08 \x01(\t\x12\x0f\n\x07\x63nspell\x18\t \x01(\t\x12\x0e\n\x06market\x18\n \x01(\t\x12\x10\n\x08\x65xchange\x18\x0b \x01(\t\x12\x11\n\tcurr_type\x18\x0c \x01(\t\x12\x13\n\x0blist_status\x18\r \x01(\t\x12\x11\n\tlist_date\x18\x0e \x01(\t\x12\x13\n\x0b\x64\x65list_date\x18\x0f \x01(\t\x12\r\n\x05is_hs\x18\x10 \x01(\t2\xcc\x01\n\x0cStockService\x12\x62\n\x0cGetStockInfo\x12!.api.crawler.v1.StockBasicRequest\x1a\x1a.api.crawler.v1.StockBasic\"\x13\x82\xd3\xe4\x93\x02\r\x12\x0b/stock/{id}\x12X\n\x0cGetIndexInfo\x12\x1c.api.crawler.v1.IndexRequest\x1a\x15.api.crawler.v1.Index\"\x13\x82\xd3\xe4\x93\x02\r\x12\x0b/index/{id}B-\n\x0e\x61pi.crawler.v1P\x01Z\x19gostock/api/crawler/v1;v1b\x06proto3')



_STOCKBASICREQUEST = DESCRIPTOR.message_types_by_name['StockBasicRequest']
_STOCKBASIC = DESCRIPTOR.message_types_by_name['StockBasic']
StockBasicRequest = _reflection.GeneratedProtocolMessageType('StockBasicRequest', (_message.Message,), {
  'DESCRIPTOR' : _STOCKBASICREQUEST,
  '__module__' : 'api.crawler.v1.stock_info_pb2'
  # @@protoc_insertion_point(class_scope:api.crawler.v1.StockBasicRequest)
  })
_sym_db.RegisterMessage(StockBasicRequest)

StockBasic = _reflection.GeneratedProtocolMessageType('StockBasic', (_message.Message,), {
  'DESCRIPTOR' : _STOCKBASIC,
  '__module__' : 'api.crawler.v1.stock_info_pb2'
  # @@protoc_insertion_point(class_scope:api.crawler.v1.StockBasic)
  })
_sym_db.RegisterMessage(StockBasic)

_STOCKSERVICE = DESCRIPTOR.services_by_name['StockService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\016api.crawler.v1P\001Z\031gostock/api/crawler/v1;v1'
  _STOCKSERVICE.methods_by_name['GetStockInfo']._options = None
  _STOCKSERVICE.methods_by_name['GetStockInfo']._serialized_options = b'\202\323\344\223\002\r\022\013/stock/{id}'
  _STOCKSERVICE.methods_by_name['GetIndexInfo']._options = None
  _STOCKSERVICE.methods_by_name['GetIndexInfo']._serialized_options = b'\202\323\344\223\002\r\022\013/index/{id}'
  _STOCKBASICREQUEST._serialized_start=110
  _STOCKBASICREQUEST._serialized_end=273
  _STOCKBASIC._serialized_start=276
  _STOCKBASIC._serialized_end=559
  _STOCKSERVICE._serialized_start=562
  _STOCKSERVICE._serialized_end=766
# @@protoc_insertion_point(module_scope)
