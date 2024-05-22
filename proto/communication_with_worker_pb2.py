# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: communication_with_worker.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x63ommunication_with_worker.proto\"\'\n\x14IdleHeartbeatRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\":\n\x15IdleHeartbeatResponse\x12!\n\x06status\x18\x01 \x01(\x0e\x32\x11.WorkerStatusEnum\"@\n\x0e\x44\x61tasetRequest\x12\x13\n\x0b\x64\x61tasetPath\x18\x01 \x01(\t\x12\x19\n\x07\x64\x61taset\x18\x02 \x01(\x0b\x32\x08.Dataset\"!\n\x0f\x44\x61tasetResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\"\x1d\n\x07\x44\x61taset\x12\x12\n\x04rows\x18\x01 \x03(\x0b\x32\x04.Row\"[\n\x0cModelRequest\x12\x11\n\tmodelPath\x18\x01 \x01(\t\x12\r\n\x05\x63hunk\x18\x02 \x01(\x0c\x12\x13\n\x0bweightsPath\x18\x03 \x01(\t\x12\x14\n\x0cweightsChunk\x18\x04 \x01(\x0c\"2\n\rModelResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x11\n\tmodelPath\x18\x02 \x01(\t\"\x15\n\x03Row\x12\x0e\n\x06values\x18\x01 \x03(\t\"\x10\n\x0e\x43omputeRequest\"0\n\x0f\x43omputeResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\r\n\x05\x63hunk\x18\x02 \x01(\x0c*&\n\x10WorkerStatusEnum\x12\x08\n\x04\x42USY\x10\x00\x12\x08\n\x04IDLE\x10\x01\x32\xe7\x01\n\rWorkerService\x12>\n\rIdleHeartbeat\x12\x15.IdleHeartbeatRequest\x1a\x16.IdleHeartbeatResponse\x12\x34\n\x0f\x44\x61tasetTransfer\x12\x0f.DatasetRequest\x1a\x10.DatasetResponse\x12\x30\n\rModelTransfer\x12\r.ModelRequest\x1a\x0e.ModelResponse\"\x00\x12.\n\x07\x43ompute\x12\x0f.ComputeRequest\x1a\x10.ComputeResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'communication_with_worker_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_WORKERSTATUSENUM']._serialized_start=504
  _globals['_WORKERSTATUSENUM']._serialized_end=542
  _globals['_IDLEHEARTBEATREQUEST']._serialized_start=35
  _globals['_IDLEHEARTBEATREQUEST']._serialized_end=74
  _globals['_IDLEHEARTBEATRESPONSE']._serialized_start=76
  _globals['_IDLEHEARTBEATRESPONSE']._serialized_end=134
  _globals['_DATASETREQUEST']._serialized_start=136
  _globals['_DATASETREQUEST']._serialized_end=200
  _globals['_DATASETRESPONSE']._serialized_start=202
  _globals['_DATASETRESPONSE']._serialized_end=235
  _globals['_DATASET']._serialized_start=237
  _globals['_DATASET']._serialized_end=266
  _globals['_MODELREQUEST']._serialized_start=268
  _globals['_MODELREQUEST']._serialized_end=359
  _globals['_MODELRESPONSE']._serialized_start=361
  _globals['_MODELRESPONSE']._serialized_end=411
  _globals['_ROW']._serialized_start=413
  _globals['_ROW']._serialized_end=434
  _globals['_COMPUTEREQUEST']._serialized_start=436
  _globals['_COMPUTEREQUEST']._serialized_end=452
  _globals['_COMPUTERESPONSE']._serialized_start=454
  _globals['_COMPUTERESPONSE']._serialized_end=502
  _globals['_WORKERSERVICE']._serialized_start=545
  _globals['_WORKERSERVICE']._serialized_end=776
# @@protoc_insertion_point(module_scope)
