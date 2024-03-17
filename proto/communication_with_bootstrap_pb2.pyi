from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

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

class JoinRequest(_message.Message):
    __slots__ = ("address", "specs")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    address: Address
    specs: Specs
    def __init__(self, address: _Optional[_Union[Address, _Mapping]] = ..., specs: _Optional[_Union[Specs, _Mapping]] = ...) -> None: ...

class JoinResponse(_message.Message):
    __slots__ = ("uuid", "existing_peers")
    UUID_FIELD_NUMBER: _ClassVar[int]
    EXISTING_PEERS_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    existing_peers: _containers.RepeatedCompositeFieldContainer[Address]
    def __init__(self, uuid: _Optional[str] = ..., existing_peers: _Optional[_Iterable[_Union[Address, _Mapping]]] = ...) -> None: ...

class HeartbeatRequest(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class HeartbeatResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class UpdateIdleRequest(_message.Message):
    __slots__ = ("address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: Address
    def __init__(self, address: _Optional[_Union[Address, _Mapping]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IdleWorkersResponse(_message.Message):
    __slots__ = ("idle_workers",)
    IDLE_WORKERS_FIELD_NUMBER: _ClassVar[int]
    idle_workers: _containers.RepeatedCompositeFieldContainer[Address]
    def __init__(self, idle_workers: _Optional[_Iterable[_Union[Address, _Mapping]]] = ...) -> None: ...
