from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class JoinRequest(_message.Message):
    __slots__ = ("CPU", "RAM", "Storage")
    CPU_FIELD_NUMBER: _ClassVar[int]
    RAM_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    CPU: str
    RAM: str
    Storage: str
    def __init__(self, CPU: _Optional[str] = ..., RAM: _Optional[str] = ..., Storage: _Optional[str] = ...) -> None: ...

class JoinResponse(_message.Message):
    __slots__ = ("existing_peers",)
    EXISTING_PEERS_FIELD_NUMBER: _ClassVar[int]
    existing_peers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, existing_peers: _Optional[_Iterable[str]] = ...) -> None: ...
