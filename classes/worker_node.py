import grpc
import sys

sys.path.append("../proto")
import communication_with_worker_pb2_grpc
from concurrent import futures


# The WorkerNode class is a parent class for the StorageWorker and ComputationWorker classes. The WorkerNode class has
# methods to send heartbeats, acknowledgment of working status, and acknowledgment of task completion to the master node.
# The StorageWorker class has methods to store a dataset and send a dataset to a peer. The ComputationWorker class has
# methods to perform computation on data, store computation results, and send results to a peer.
class WorkerNode(communication_with_worker_pb2_grpc.WorkerServiceServicer):
    def __init__(self, bootstrap_server_address, IP, port, uuid):
        self.bootstrap_server_address = bootstrap_server_address
        self.IP = IP
        self.port = port
        self.uuid = uuid

    def worker(self):
        # Worker thread.
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        print(f"Worker node running on {self.IP}:{self.port}")
        worker_service = WorkerNode(self.bootstrap_server_address, self.IP, self.port, self.uuid)
        communication_with_worker_pb2_grpc.add_WorkerServiceServicer_to_server(
            worker_service, server
        )
        server.add_insecure_port(f'{self.IP}:{self.port}')
        print(f"Worker node running on {self.IP}:{self.port}")
        server.start()
        server.wait_for_termination()

    def send_heart_beat(self):
        # Send heartbeat to master.
        pass

    def send_ack_working(self):
        # Send acknowledgment of working status to master.
        pass

    def send_ack_done_working(self):
        # Send acknowledgment of task completion to master.
        pass


class StorageWorker(WorkerNode):
    def __init__(self, master):
        super().__init__(master)

    def store_dataset(self, dataset):
        # Store dataset.
        pass

    def send_dataset(self, peer):
        # Send dataset to a peer.
        pass


class ComputationWorker(WorkerNode):
    def __init__(self, master):
        super().__init__(master)

    def compute(self, data):
        # Perform computation on data.
        pass

    def store_results(self, results):
        # Store computation results.
        pass

    def send_results(self, peer):
        # Send results to a peer.
        pass
