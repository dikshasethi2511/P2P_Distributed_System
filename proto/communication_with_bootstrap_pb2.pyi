from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileTypleEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASET: _ClassVar[FileTypleEnum]
    MODEL: _ClassVar[FileTypleEnum]
DATASET: FileTypleEnum
MODEL: FileTypleEnum

class Address(_message.Message):
    __slots__ = ("IP", "port")
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    IP: str
    port: str
    def __init__(self, IP: _Optional[str] = ..., port: _Optional[str] = ...) -> None: ...

class Shards(_message.Message):
    __slots__ = ("address", "shard")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SHARD_FIELD_NUMBER: _ClassVar[int]
    address: Address
    shard: int
    def __init__(self, address: _Optional[_Union[Address, _Mapping]] = ..., shard: _Optional[int] = ...) -> None: ...

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

class UpdateStorageRequest(_message.Message):
    __slots__ = ("address", "path", "type", "workers")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKERS_FIELD_NUMBER: _ClassVar[int]
    address: Address
    path: str
    type: FileTypleEnum
    workers: _containers.RepeatedCompositeFieldContainer[Shards]
    def __init__(self, address: _Optional[_Union[Address, _Mapping]] = ..., path: _Optional[str] = ..., type: _Optional[_Union[FileTypleEnum, str]] = ..., workers: _Optional[_Iterable[_Union[Shards, _Mapping]]] = ...) -> None: ...

class UpdateStorageResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class GetStorageRequest(_message.Message):
    __slots__ = ("path", "address")
    PATH_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    path: str
    address: Address
    def __init__(self, path: _Optional[str] = ..., address: _Optional[_Union[Address, _Mapping]] = ...) -> None: ...

class GetStorageResponse(_message.Message):
    __slots__ = ("status", "workers")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    WORKERS_FIELD_NUMBER: _ClassVar[int]
    status: str
    workers: _containers.RepeatedCompositeFieldContainer[Shards]
    def __init__(self, status: _Optional[str] = ..., workers: _Optional[_Iterable[_Union[Shards, _Mapping]]] = ...) -> None: ...
