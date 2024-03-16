import sys
import grpc
import time
from threading import Event, Thread
sys.path.append("../proto")
import communication_with_bootstrap_pb2
import communication_with_bootstrap_pb2_grpc


class Peer:
    def __init__(self, bootstrap_server_address, IP, port):
        self.bootstrap_server_address = bootstrap_server_address
        self.IP = IP
        self.port = port
        self.exit_flag = Event()

    def connect_to_bootstrap_server(self, CPU, RAM, storage):
        with grpc.insecure_channel(self.bootstrap_server_address) as channel:
            stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(channel)
            self.register_peer(stub, CPU, RAM, storage)

    def register_peer(self, stub, CPU, RAM, storage):
        request = communication_with_bootstrap_pb2.JoinRequest(
            address=communication_with_bootstrap_pb2.Address(
                IP=self.IP, port=self.port
            ),
            specs=communication_with_bootstrap_pb2.Specs(
                CPU=CPU, RAM=RAM, storage=storage
            ),
        )
        response = stub.JoinNetwork(request)
        if response.existing_peers:
            self.uuid = response.uuid
            print(
                f"Received existing peers from Bootstrap Server: {response.existing_peers}"
            )
            self.exit_flag.set()
            thread1 = Thread(target=self.send_heartbeat, args=())
            thread1.start()

    def send_heartbeat(self):
        while self.exit_flag.is_set():
            with grpc.insecure_channel(self.bootstrap_server_address) as channel:
                stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(
                    channel
                )
                request = communication_with_bootstrap_pb2.HeartbeatRequest(
                    uuid=self.uuid,
                )
                status = stub.ActiveHeartbeat(request)
            print(status)
            time.sleep(3)

    
