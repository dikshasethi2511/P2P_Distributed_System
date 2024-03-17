import sys
import grpc
import time
from threading import Event, Thread

sys.path.append("../proto")
import communication_with_bootstrap_pb2
import communication_with_bootstrap_pb2_grpc
from worker_node import WorkerNode
from master_node import MasterNode


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
            worker = WorkerNode(
                self.bootstrap_server_address, self.IP, self.port, self.uuid
            )

            thread1 = Thread(target=self.send_heartbeat)

            thread2 = Thread(target=worker.worker)
            thread3 = Thread(target=self.ask_to_be_master)

            thread1.start()
            thread2.start()
            thread3.start()

            thread1.join()
            thread2.join()
            thread3.join()

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
            print("Heartbeat status: ", status.status)
            time.sleep(45)

    def ask_to_be_master(self):
        response = "n"
        while self.exit_flag.is_set():
            if response == "y":
                master = MasterNode(
                    self.bootstrap_server_address, self.IP, self.port, self.uuid
                )
                master.run_master()
            response = input("Do you want to be the master? (y/n): ")
