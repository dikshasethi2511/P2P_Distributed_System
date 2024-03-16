from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JoinRequest(_message.Message):
    __slots__ = ("address", "specs")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    address: Address
    specs: Specs
    def __init__(self, address: _Optional[_Union[Address, _Mapping]] = ..., specs: _Optional[_Union[Specs, _Mapping]] = ...) -> None: ...

class Address(_message.Message):
    __slots__ = ("IP", "port")
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    IP: str
    port: str
    def __init__(self, IP: _Optional[str] = ..., port: _Optional[str] = ...) -> None: ...

class Specs(_message.Message):
    __slots__ = ("CPU", "RAM", "storage")
    CPU_FIELD_NUMBER: _ClassVar[int]
    RAM_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    CPU: str
    RAM: str
    storage: str
    def __init__(self, CPU: _Optional[str] = ..., RAM: _Optional[str] = ..., storage: _Optional[str] = ...) -> None: ...

class JoinResponse(_message.Message):
    __slots__ = ("existing_peers",)
    EXISTING_PEERS_FIELD_NUMBER: _ClassVar[int]
    existing_peers: _containers.RepeatedCompositeFieldContainer[Address]
    def __init__(self, existing_peers: _Optional[_Iterable[_Union[Address, _Mapping]]] = ...) -> None: ...
