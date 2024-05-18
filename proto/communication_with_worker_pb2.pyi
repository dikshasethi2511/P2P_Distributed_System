from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WorkerStatusEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUSY: _ClassVar[WorkerStatusEnum]
    IDLE: _ClassVar[WorkerStatusEnum]
BUSY: WorkerStatusEnum
IDLE: WorkerStatusEnum

class IdleHeartbeatRequest(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class IdleHeartbeatResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: WorkerStatusEnum
    def __init__(self, status: _Optional[_Union[WorkerStatusEnum, str]] = ...) -> None: ...

class DatasetRequest(_message.Message):
    __slots__ = ("datasetPath", "dataset")
    DATASETPATH_FIELD_NUMBER: _ClassVar[int]
    DATASET_FIELD_NUMBER: _ClassVar[int]
    datasetPath: str
    dataset: Dataset
    def __init__(self, datasetPath: _Optional[str] = ..., dataset: _Optional[_Union[Dataset, _Mapping]] = ...) -> None: ...

class DatasetResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class Dataset(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[Row]
    def __init__(self, rows: _Optional[_Iterable[_Union[Row, _Mapping]]] = ...) -> None: ...

class ModelRequest(_message.Message):
    __slots__ = ("modelPath", "chunk", "weightsPath", "weightsChunk")
    MODELPATH_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    WEIGHTSPATH_FIELD_NUMBER: _ClassVar[int]
    WEIGHTSCHUNK_FIELD_NUMBER: _ClassVar[int]
    modelPath: str
    chunk: bytes
    weightsPath: str
    weightsChunk: bytes
    def __init__(self, modelPath: _Optional[str] = ..., chunk: _Optional[bytes] = ..., weightsPath: _Optional[str] = ..., weightsChunk: _Optional[bytes] = ...) -> None: ...

class ModelResponse(_message.Message):
    __slots__ = ("status", "modelPath")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MODELPATH_FIELD_NUMBER: _ClassVar[int]
    status: str
    modelPath: str
    def __init__(self, status: _Optional[str] = ..., modelPath: _Optional[str] = ...) -> None: ...

class Row(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class ComputeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ComputeResponse(_message.Message):
    __slots__ = ("status", "chunk")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    status: str
    chunk: bytes
    def __init__(self, status: _Optional[str] = ..., chunk: _Optional[bytes] = ...) -> None: ...
