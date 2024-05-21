# The master node is the node that wants to initiate the task. It is responsible for choosing the workers, initiating the
# tasks, sending heartbeats to the working nodes, creating data shards, initiating data distribution, uploading, deleting,
# downloading, and updating the dataset, and adding tasks to the queue.

import pickle
import grpc
import sys
import os
import random

import joblib
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

sys.path.append("../proto")
import communication_with_bootstrap_pb2
import communication_with_bootstrap_pb2_grpc
import communication_with_worker_pb2
import communication_with_worker_pb2_grpc
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()
from task_queue import TaskQueue
import csv
from joblib import dump
import time


class MasterNode:
    def __init__(self, bootstrap_server_address, IP, port, uuid):
        self.working_nodes = []
        self.alloted_workers_to_shards = {}
        self.number_of_tasks = 0
        self.leftover_count = 0
        self.task_queue = TaskQueue()
        self.data_locations = {}
        self.bootstrap_server_address = bootstrap_server_address
        self.IP = IP
        self.port = port
        self.uuid = uuid
        self.storageInformation = {}
        self.modelLocations = {}
        self.storage_latencies = []
        self.computation_latencies = []

    def run_master(self):
        # Run master node.
        self.request_idle_workers()
        print("Master Node Menu")
        print(
            "1. Upload Dataset\n2. Upload Code\n3. Compute\n4. Plot Latency Graph\n5. Exit"
        )
        inp = input("Enter your choice: ")
        if inp == "1":
            dataset = input("Enter the dataset file path: ")
            # /mnt/c/Users/hp/Desktop/IIITD/BTP/P2P_Distributed_System/data/Iris.csv
            latency, _ = self.measure_latency(self.store_and_transmit_dataset, dataset)
            print(f"Latency: {latency}")
            self.storage_latencies.append(latency)
            with open("storage_latencies.txt", "a") as f:
                for latency in self.storage_latencies:
                    f.write(f"{latency}\n")

        elif inp == "2":
            dataset = input("Enter the dataset file path: ")
            code = input("Enter the code file path: ")
            # /mnt/c/Users/hp/Desktop/IIITD/BTP/P2P_Distributed_System/models/model.py
            # /mnt/c/Users/hp/Desktop/IIITD/BTP/P2P_Distributed_System/models/initial_knn_model.joblib
            weights = input("Enter the weights file path: ")
            self.initiate_tasks(code, dataset, weights)
        elif inp == "3":
            dataset = input("Enter the dataset file path: ")
            latency, _ = self.measure_latency(self.compute, dataset)
            self.computation_latencies.append(latency)
            with open("compute_latencies.txt", "a") as f:
                for latency in self.computation_latencies:
                    f.write(f"{latency}\n")
            self.federated_averaging(
                "/mnt/c/Users/hp/Desktop/IIITD/BTP/P2P_Distributed_System/communication/weights",
                1,
            )
        elif inp == "4":
            self.plot_latencies()
        elif inp == "5":
            exit()

    def store_and_transmit_dataset(self, dataset):
        if self.get_storage_information(dataset):
            print(f"Dataset {dataset} already exists in storage.")
            return
        self.upload_dataset(dataset)
        self.initiate_data_distribution(self.data_locations, self.working_nodes)
        self.add_leftover_tasks()
        self.transmit_dataset(dataset)

    def compute(self, datasetpath):
        peers = self.get_storage_information(datasetpath)
        if not peers:
            print(
                f"Dataset {datasetpath} not found in storage. Upload the dataset first."
            )
            return
        print(f"Peers: {peers}")
        for peer in peers:
            status = self.get_idle_ack(peer)
            print(f"Status: {status}")
            if status == communication_with_worker_pb2.IDLE:
                self.update_bootstrap(peer, "BUSY")
                self.compute_at_peer(peer)
                self.update_bootstrap(peer, "IDLE")

    def request_idle_workers(self):
        with grpc.insecure_channel(self.bootstrap_server_address) as channel:
            stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(channel)
            try:
                response = stub.GetIdleWorkers(communication_with_bootstrap_pb2.Empty())
                max_workers = int(os.getenv("UPPER_LIMIT_FOR_WORKERS", default=10))
                num_workers = min(len(response.idle_workers), max_workers)
                # Take user input or use a predetermined number of workers.
                required_workers = int(input("Enter the number of tasks to assign: "))
                self.number_of_tasks = required_workers
                self.working_nodes = self.choose_workers(response.idle_workers)

            except grpc.RpcError as e:
                print(f"Error: gRPC communication failed - {e}")

    def choose_workers(self, idle_workers):
        # Choose available workers for a task.
        # Filter out own address from the list of idle workers.
        idle_workers_chosen = [
            address
            for address in idle_workers
            if address.IP != self.IP or address.port != self.port
        ]

        if len(idle_workers_chosen) < self.number_of_tasks:
            self.leftover_count = self.number_of_tasks - len(idle_workers_chosen)

        available_workers = self.number_of_tasks - self.leftover_count
        available_workers = min(available_workers, len(idle_workers_chosen))
        chosen_workers = random.sample(idle_workers_chosen, available_workers)
        print(f"Chosen workers: {chosen_workers}")
        return chosen_workers

    def initiate_tasks(self, codepath, datasetpath, weights):
        # Initiate tasks and distribute to chosen workers.
        # Send the code to allocated workers.
        peers = self.get_storage_information(datasetpath)
        if not peers:
            print(
                f"Dataset {datasetpath} not found in storage. Upload the dataset first."
            )
            return
        print(f"Peers: {peers}")
        for peer in peers:
            status = self.get_idle_ack(peer)
            print(f"Status: {status}")
            if status == communication_with_worker_pb2.IDLE:
                self.update_bootstrap(peer, "BUSY")
                self.transmit_model_peer(codepath, peer, weights)
                self.update_bootstrap(peer, "IDLE")

    def send_heart_beat(self):
        # Send heartbeat to working nodes.
        pass

    def create_shards(self, data):
        # Create data shards.
        pass

    def initiate_data_distribution(self, data_locations, peers):
        # Distribute one shard from each data location base folder to a peer.
        allocated_shard_count = 1
        for peer in peers:
            peer_address = (peer.IP, peer.port)
            self.alloted_workers_to_shards[peer_address] = []
            for base_folder in data_locations.keys():
                file_path = self.data_locations[base_folder][allocated_shard_count]
                self.alloted_workers_to_shards[peer_address].append(
                    (base_folder, allocated_shard_count, file_path)
                )
            allocated_shard_count += 1

    def add_leftover_tasks(self):
        # For each base folder, find the remaining shards and add them to the task queue.
        for remaining_count in range(
            self.number_of_tasks - self.leftover_count + 1, self.number_of_tasks + 1
        ):
            for base_folder in self.data_locations.keys():
                file_path = self.data_locations[base_folder][remaining_count]
                self.task_queue.enqueue((base_folder, remaining_count, file_path))

        # print(f"Task Queue: {self.task_queue.queue}")

    def upload_dataset(self, dataset_path):
        # Upload dataset to bootstrap server or distribute to peers.
        directory_path = os.path.dirname(dataset_path)

        with open(dataset_path, "r", newline="") as csvfile:
            csvreader = csv.reader(csvfile)
            content = list(csvreader)  # Read CSV content into a list

            # Copy the first line to all shards
            first_line = content[0]

        # Calculate shard size and ensure all shards are of equal size by dropping rows if necessary
        total_rows = len(content) - 1
        shard_size = total_rows // self.number_of_tasks

        # If there's a remainder, drop the extra rows
        rows_to_use = shard_size * self.number_of_tasks
        content = [first_line] + content[1 : rows_to_use + 1]

        # Create a directory for the file shards
        base_name, extension = os.path.splitext(dataset_path)
        self.data_locations[directory_path] = {}

        # Divide the content into shards and store each shard in a separate file
        start = 1
        print(f"Shard size: {shard_size}")
        print(f"Number of tasks: {self.number_of_tasks}")
        for i in range(self.number_of_tasks):
            shard_content = [first_line] + content[start : start + shard_size]
            shard_file_path = os.path.join(
                directory_path, f"{base_name}_shard_{i + 1}{extension}"
            )

            # Add the shard file path to the data locations dictionary.
            # Store base folder and the shard count as the key.
            self.data_locations[directory_path][i + 1] = shard_file_path

            with open(shard_file_path, "w", newline="") as shard_file:
                shard_writer = csv.writer(shard_file)
                shard_writer.writerows(shard_content)
            start += shard_size

    def delete_dataset(self, dataset):
        # Delete dataset.
        pass

    def download_dataset(self, dataset, peer):
        # Download dataset from bootstrap server or peer.
        pass

    def update_dataset(self, dataset, new_data):
        # Update dataset.
        pass

    def save_global_model_weights(self, weights):
        # Save the global model weights
        # Example:
        dump(weights, "../weights/global_model.joblib")

    def federated_averaging(self, folder_path, num_iterations):
        # Initialize lists to hold the weights from each model
        weights_list = []
        classes_list = []

        # Loop through the files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".joblib"):
                file_path = os.path.join(folder_path, filename)
                # Load the model from the joblib file
                model = joblib.load(file_path)
                if isinstance(model, KNeighborsClassifier):
                    weights_list.append(model._fit_X)
                    classes_list.append(model.classes_)
                else:
                    raise ValueError(f"Unexpected model type in file {file_path}")

        # Check if any weights were loaded
        if not weights_list:
            raise ValueError("No joblib files found in the specified folder.")

        # Averaging the weights
        averaged_weights = np.mean(weights_list, axis=0)
        averaged_classes = np.unique(np.concatenate(classes_list))

        # Create a new KNeighborsClassifier and set its attributes
        final_model = KNeighborsClassifier()
        final_model._fit_X = averaged_weights
        final_model.classes_ = averaged_classes
        # Note: Additional attributes of KNeighborsClassifier may need to be set

        # Save the averaged model to a new joblib file
        output_file = os.path.join(folder_path, "averaged_weights.joblib")
        joblib.dump(final_model, output_file)

        print(f"Averaged model saved to {output_file}")

    def transmit_dataset(self, dataset_path):
        for peer in self.alloted_workers_to_shards.keys():
            for shard in self.alloted_workers_to_shards[peer]:
                status = self.get_idle_ack(peer)
                print(f"Status: {status}")
                if status == communication_with_worker_pb2.IDLE:
                    self.update_bootstrap(peer, "BUSY")
                    self.transmit_dataset_peer(shard, peer, dataset_path)
                    self.update_bootstrap(peer, "IDLE")
        self.update_storage_information(dataset_path, 0)

    def transmit_dataset_peer(self, data, peer, dataset_path):
        with open(data[2], "r", newline="") as csvfile:
            dataset = list(csv.reader(csvfile))

        components = data[2].split("/")  # Split the path into components
        components[-2] = "compute"
        name, extention = components[-1].split(".")
        components[-1] = name.split("_")[0] + "." + extention
        filepath = "/".join(components)
        print(f"Filepath: {filepath}")

        with grpc.insecure_channel(f"{peer[0]}:{peer[1]}") as channel:
            stub = communication_with_worker_pb2_grpc.WorkerServiceStub(channel)
            request = communication_with_worker_pb2.DatasetRequest(
                datasetPath=filepath,
                dataset=communication_with_worker_pb2.Dataset(
                    rows=[
                        communication_with_worker_pb2.Row(values=row) for row in dataset
                    ]
                ),
            )
            response = stub.DatasetTransfer(request)
            print(f"Dataset transmitted to {peer} with status: {response.status}")

            if response.status == "SUCCESS":
                if self.storageInformation.get(dataset_path):
                    self.storageInformation[dataset_path].append(peer)
                else:
                    self.storageInformation[dataset_path] = [peer]
            print(f"Storage Information: {self.storageInformation}")

    def compute_at_peer(self, peer):
        with grpc.insecure_channel(f"{peer[0]}:{peer[1]}") as channel:
            stub = communication_with_worker_pb2_grpc.WorkerServiceStub(channel)
            request = communication_with_worker_pb2.ComputeRequest()
            response = stub.Compute(request)
            print(f"Computation completed at {peer} with status: {response.status}")

            # Create a directory called weights if not present.
            if not os.path.exists("weights"):
                os.makedirs("weights")

            # Save the bytes received in response.chunk to a file called weights.joblib.
            # For each peer append its address to the file name.
            with open(f"weights/weights_{peer[0]}_{peer[1]}.joblib", "wb") as f:
                f.write(response.chunk)

    def transmit_model_peer(self, filepath, peer, weights_filepath):
        with grpc.insecure_channel(f"{peer[0]}:{peer[1]}") as channel:
            stub = communication_with_worker_pb2_grpc.WorkerServiceStub(channel)

            # Construct the store file paths
            components = filepath.split("/")
            components[-2] = "compute"
            storefilepath = "/".join(components)

            components = weights_filepath.split("/")
            components[-2] = "compute"
            storeweightspath = "/".join(components)

            # Serialize the weights file
            with open(weights_filepath, "rb") as f_weights:
                weights_data = f_weights.read()
                pickled_weights = pickle.dumps(weights_data)

            # Open the model file and read it in chunks
            CHUNK_SIZE = 4096
            with open(filepath, "rb") as f:
                while True:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break

                    # Create a ModelRequest message with the current chunk and file path
                    model_request = communication_with_worker_pb2.ModelRequest(
                        modelPath=storefilepath,
                        chunk=chunk,
                        weightsPath=storeweightspath,
                        weightsChunk=pickled_weights,
                    )

                    # Call the ModelTransfer RPC method with the ModelRequest
                    model_response = stub.ModelTransfer(model_request)

                    # Handle the response, if needed
                    print("Received status:", model_response.status)
                    print("Path received:", model_response.modelPath)

        print("Model transmission completed to peer:", peer)

    def get_idle_ack(self, peer):
        print(f"Checking status of {peer}")
        with grpc.insecure_channel(f"{peer[0]}:{peer[1]}") as channel:
            stub = communication_with_worker_pb2_grpc.WorkerServiceStub(channel)
            response = stub.IdleHeartbeat(
                communication_with_worker_pb2.IdleHeartbeatRequest(message="Idle?")
            )
        return response.status

    def update_bootstrap(self, peer, state):
        with grpc.insecure_channel(self.bootstrap_server_address) as channel:
            stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(channel)
            request = communication_with_bootstrap_pb2.UpdateIdleRequest(
                address=communication_with_bootstrap_pb2.Address(
                    IP=peer[0], port=peer[1]
                ),
            )
            if state == "IDLE":
                stub.UpdateIdleWorker(request)
            elif state == "BUSY":
                stub.UpdateNotIdleWorker(request)

    def update_storage_information(self, dataset_path, type):
        with grpc.insecure_channel(self.bootstrap_server_address) as channel:
            stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(channel)
            peers = []
            for peer in self.storageInformation[dataset_path]:
                peers.append(
                    communication_with_bootstrap_pb2.Address(IP=peer[0], port=peer[1])
                )
            request = communication_with_bootstrap_pb2.UpdateStorageRequest(
                address=communication_with_bootstrap_pb2.Address(
                    IP=self.IP, port=self.port
                ),
                path=dataset_path,
                type=0,
                workers=peers,
            )
            if type == 0:
                request.type = communication_with_bootstrap_pb2.FileTypleEnum.DATASET
            else:
                request.type = communication_with_bootstrap_pb2.FileTypleEnum.MODEL
            response = stub.UpdateStorage(request)
            print(f"Storage information updated with status: {response.status}")

    def get_storage_information(self, dataset_path):
        with grpc.insecure_channel(self.bootstrap_server_address) as channel:
            stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(channel)
            request = communication_with_bootstrap_pb2.GetStorageRequest(
                path=dataset_path,
                address=communication_with_bootstrap_pb2.Address(
                    IP=self.IP, port=self.port
                ),
            )
            response = stub.GetStorage(request)
            print(f"Storage information for {dataset_path}: {response.status}")

        if response.status == "SUCCESS":
            peers = []
            for peer in response.workers:
                peers.append((peer.IP, peer.port))
            return peers
        return None

    def plot_latencies(self):
        # Plot storage latencies
        plt.figure(figsize=(12, 6))
        with open("storage_latencies.txt", "r") as f:
            self.storage_latencies = [float(latency) for latency in f.readlines()]

        print(self.storage_latencies)
        plt.plot(self.storage_latencies, label="Storage Latency")
        plt.xlabel("Operation")
        plt.ylabel("Latency (s)")
        plt.title("Storage Latency")
        plt.legend()
        plt.grid(True)
        plt.savefig("storage_latency.png")  # Save the plot as a file
        plt.close()

        # Plot computation latencies
        plt.figure(figsize=(12, 6))
        with open("compute_latencies.txt", "r") as f:
            self.computation_latencies = [float(latency) for latency in f.readlines()]
        plt.plot(self.computation_latencies, label="Computation Latency")
        plt.xlabel("Operation")
        plt.ylabel("Latency (s)")
        plt.title("Computation Latency")
        plt.legend()
        plt.grid(True)
        plt.savefig("compute_latency.png")  # Save the plot as a file
        plt.close()

    def measure_latency(self, func, *args, **kwargs):
        start_time = time.time()
        print(f"s: {start_time}")
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"e: {end_time}")
        latency = end_time - start_time
        print(f"Latency: {latency}")
        print()
        return latency, result
