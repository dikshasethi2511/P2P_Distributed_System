import grpc
import sys

sys.path.append("../proto")
import communication_with_worker_pb2_grpc
import communication_with_worker_pb2
from concurrent import futures
import csv
import os


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
        self.idle = True

    def worker(self):
        # Worker thread.
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        print(f"Worker node running on {self.IP}:{self.port}")
        worker_service = WorkerNode(
            self.bootstrap_server_address, self.IP, self.port, self.uuid
        )
        communication_with_worker_pb2_grpc.add_WorkerServiceServicer_to_server(
            worker_service, server
        )
        server.add_insecure_port(f"{self.IP}:{self.port}")
        print(f"Worker node running on {self.IP}:{self.port}")
        server.start()
        server.wait_for_termination()

    def DatasetTransfer(self, request, context):
        self.idle = False
        return self.store_dataset(request)

    def IdleHeartbeat(self, request, context):
        if self.idle:
            return communication_with_worker_pb2.IdleHeartbeatResponse(
                status=communication_with_worker_pb2.IDLE
            )
        return communication_with_worker_pb2.IdleHeartbeatResponse(
            status=communication_with_worker_pb2.BUSY
        )

    def ModelTransfer(self, request, context):
        self.idle = False
        # Define the directory path and ensure it exists
        last_slash_index = request.modelPath.rfind("/")
        output_directory = request.modelPath[:last_slash_index] + "/" + str(self.port)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        try:
            # Ensure the directory exists
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            # Define the file path to store the model
            output_file = os.path.join(
                output_directory, os.path.basename(request.modelPath)
            )

            # Write the received chunk to the model file
            with open(output_file, "ab") as f:
                f.write(request.chunk)

            return communication_with_worker_pb2.ModelResponse(status="SUCCESS")
        except Exception as e:
            return communication_with_worker_pb2.ModelResponse(
                status=f"ERROR: {str(e)}"
            )
        finally:
            self.idle = True

    def send_heart_beat(self):
        # Send heartbeat to master.
        pass

    def send_ack_working(self):
        # Send acknowledgment of working status to master.
        pass

    def send_ack_done_working(self):
        # Send acknowledgment of task completion to master.
        pass

    def store_dataset(self, request):
        # Process the received dataset
        dataset_path = request.datasetPath
        dataset = request.dataset

        # Define the directory path and ensure it exists
        last_slash_index = dataset_path.rfind("/")
        output_directory = dataset_path[:last_slash_index] + "/" + str(self.port)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Define the file path to store the dataset
        output_file = output_directory + "/" + os.path.split(dataset_path)[-1]

        # Write the dataset to a CSV file
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for row in dataset.rows:
                writer.writerow(row.values)

        self.idle = True
        return communication_with_worker_pb2.DatasetResponse(status="SUCCESS")


class StorageWorker(WorkerNode):
    def __init__(self, master):
        super().__init__(master)

    def store_dataset(self, request):
        # Process the received dataset
        dataset_path = request.datasetPath
        dataset = request.dataset

        # Define the directory path and ensure it exists
        output_directory = dataset_path.rsplit("/", 1) + str()
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Define the file path to store the dataset
        output_file = output_directory + os.path.split(dataset_path)[-1]

        # Write the dataset to a CSV file
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for row in dataset.rows:
                writer.writerow(row.values)

        print(f"Dataset stored in {output_file}")

        # Acknowledge the receipt of the dataset
        return communication_with_worker_pb2.DatasetResponse(status="SUCCESS")

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
