import pickle
import grpc
import sys

sys.path.append("../proto")
import communication_with_worker_pb2_grpc
import communication_with_worker_pb2
from concurrent import futures
import csv
import os
import subprocess


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
        self.modelPath = ""

    def worker(self):
        # Worker thread.
        max_message_size = 20 * 1024 * 1024  # 20 MB

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                            options=[
                                ('grpc.max_send_message_length', max_message_size),
                                ('grpc.max_receive_message_length', max_message_size),
                            ])
        print(f"Worker node running on {self.IP}:{self.port}")
        worker_service = WorkerNode(
            self.bootstrap_server_address, self.IP, self.port, self.uuid
        )
        communication_with_worker_pb2_grpc.add_WorkerServiceServicer_to_server(
            worker_service, server
        )
        server.add_insecure_port(f"[::]:{self.port}")
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

    def Compute(self, request, context):
        self.idle = False
        modelPath = self.modelPath
        try:
            if os.path.exists(modelPath):
                print("Model file received successfully.")
                # Execute the Python file
                # subprocess.run(["/usr/bin/python3", output_file])
                os.system(f"python3 {modelPath}")

                # Take path of modelPath except the last part
                last_slash_index = modelPath.rfind("/")

                # Create file path with last_part as weights.joblib
                output_file = modelPath[:last_slash_index] + "/weights.joblib"

                # Read the saved weights joblib file and send it in the response
                # as bytes with the field named chunk.
                with open(output_file, "rb") as f:
                    chunk = f.read()
                    return communication_with_worker_pb2.ComputeResponse(
                        status="SUCCESS", chunk=chunk
                    )
            else:
                return communication_with_worker_pb2.ComputeResponse(
                    status="ERROR: Could not compute"
                )

        except Exception as e:
            return communication_with_worker_pb2.ModelResponse(
                status=f"ERROR: {str(e)}"
            )
        finally:
            self.idle = True

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

            print(request.chunk)
            print(request.weightsChunk)

            # Define the file path to store the model
            model_output_file = os.path.join(
                output_directory, os.path.basename(request.modelPath)
            )

            with open(model_output_file, "w") as f:
                f.write(f"PORT = {self.port}\n")

            # Write the received chunk to the model file
            with open(model_output_file, "ab") as f:
                f.write(request.chunk)

            # Deserialize the weights from the received chunk
            weights_data = pickle.loads(request.weightsChunk)

            # Define the file path to store the weights
            weights_output_file = os.path.join(
                output_directory, os.path.basename(request.weightsPath)
            )

            # Write the deserialized weights data to the weights file
            with open(weights_output_file, "wb") as f:
                f.write(weights_data)

            print("Reached here")

            if os.path.exists(model_output_file) and os.path.exists(
                weights_output_file
            ):
                print("Model and weights files received successfully.")
                # Execute the Python file if needed
                # subprocess.run(["/usr/bin/python3", model_output_file])
                # os.system(f"python3 {model_output_file}")

                self.modelPath = model_output_file

                return communication_with_worker_pb2.ModelResponse(
                    status="SUCCESS", modelPath=model_output_file
                )
            else:
                return communication_with_worker_pb2.ModelResponse(
                    status="ERROR: Files not found."
                )

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
        with open(output_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for row in dataset.rows:
                writer.writerow(row.values)

        self.idle = True
        return communication_with_worker_pb2.DatasetResponse(status="SUCCESS")


class StorageWorker(WorkerNode):
    def __init__(self, master):
        super().__init__(master)
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
