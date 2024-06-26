# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import communication_with_worker_pb2 as communication__with__worker__pb2

GRPC_GENERATED_VERSION = '1.64.0'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in communication_with_worker_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class WorkerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.IdleHeartbeat = channel.unary_unary(
                '/WorkerService/IdleHeartbeat',
                request_serializer=communication__with__worker__pb2.IdleHeartbeatRequest.SerializeToString,
                response_deserializer=communication__with__worker__pb2.IdleHeartbeatResponse.FromString,
                _registered_method=True)
        self.DatasetTransfer = channel.unary_unary(
                '/WorkerService/DatasetTransfer',
                request_serializer=communication__with__worker__pb2.DatasetRequest.SerializeToString,
                response_deserializer=communication__with__worker__pb2.DatasetResponse.FromString,
                _registered_method=True)
        self.ModelTransfer = channel.unary_unary(
                '/WorkerService/ModelTransfer',
                request_serializer=communication__with__worker__pb2.ModelRequest.SerializeToString,
                response_deserializer=communication__with__worker__pb2.ModelResponse.FromString,
                _registered_method=True)
        self.Compute = channel.unary_unary(
                '/WorkerService/Compute',
                request_serializer=communication__with__worker__pb2.ComputeRequest.SerializeToString,
                response_deserializer=communication__with__worker__pb2.ComputeResponse.FromString,
                _registered_method=True)


class WorkerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def IdleHeartbeat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DatasetTransfer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModelTransfer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Compute(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'IdleHeartbeat': grpc.unary_unary_rpc_method_handler(
                    servicer.IdleHeartbeat,
                    request_deserializer=communication__with__worker__pb2.IdleHeartbeatRequest.FromString,
                    response_serializer=communication__with__worker__pb2.IdleHeartbeatResponse.SerializeToString,
            ),
            'DatasetTransfer': grpc.unary_unary_rpc_method_handler(
                    servicer.DatasetTransfer,
                    request_deserializer=communication__with__worker__pb2.DatasetRequest.FromString,
                    response_serializer=communication__with__worker__pb2.DatasetResponse.SerializeToString,
            ),
            'ModelTransfer': grpc.unary_unary_rpc_method_handler(
                    servicer.ModelTransfer,
                    request_deserializer=communication__with__worker__pb2.ModelRequest.FromString,
                    response_serializer=communication__with__worker__pb2.ModelResponse.SerializeToString,
            ),
            'Compute': grpc.unary_unary_rpc_method_handler(
                    servicer.Compute,
                    request_deserializer=communication__with__worker__pb2.ComputeRequest.FromString,
                    response_serializer=communication__with__worker__pb2.ComputeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'WorkerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('WorkerService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class WorkerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def IdleHeartbeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/WorkerService/IdleHeartbeat',
            communication__with__worker__pb2.IdleHeartbeatRequest.SerializeToString,
            communication__with__worker__pb2.IdleHeartbeatResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DatasetTransfer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/WorkerService/DatasetTransfer',
            communication__with__worker__pb2.DatasetRequest.SerializeToString,
            communication__with__worker__pb2.DatasetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ModelTransfer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/WorkerService/ModelTransfer',
            communication__with__worker__pb2.ModelRequest.SerializeToString,
            communication__with__worker__pb2.ModelResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Compute(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/WorkerService/Compute',
            communication__with__worker__pb2.ComputeRequest.SerializeToString,
            communication__with__worker__pb2.ComputeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
