import sys
import grpc
sys.path.append('../proto')
import communication_with_bootstrap_pb2
import communication_with_bootstrap_pb2_grpc

class Peer:
    def __init__(self, bootstrap_server_address):
        self.bootstrap_server_address = bootstrap_server_address

    def connect_to_bootstrap_server(self):
        with grpc.insecure_channel(self.bootstrap_server_address) as channel:
            stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(channel)
            self.register_peer(stub)

    def register_peer(self, stub):
        request = communication_with_bootstrap_pb2.JoinRequest()
        response = stub.JoinNetwork(request)
        print(f"Received existing peers from Bootstrap Server: {response.existing_peers}")
