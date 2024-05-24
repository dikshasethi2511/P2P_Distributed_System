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
import csv
from joblib import dump
import time
import chardet


class MasterNode:
    def __init__(self, bootstrap_server_address, IP, port, uuid):
        self.working_nodes = []
        self.alloted_workers_to_shards = {}
        self.number_of_tasks = 0
        self.leftover_count = 0
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
        print(
            "Master Node Menu\n1. Upload Dataset\n2. Upload Code\n3. Compute\n4. Plot Latency Graph\n5. Exit"
        )
        inp = input("Enter your choice: ")
        if inp == "1":
            self.working_nodes = self.choose_workers(self.request_idle_workers())
            if len(self.working_nodes) == 0:
                print("No workers available. Try again later.")
                return
            dataset = input("Enter the dataset file path: ")
            latency = self.measure_latency(self.store_and_transmit_dataset, dataset)
            self.storage_latencies.append(latency)
            with open("storage_latencies.txt", "a") as f:
                for latency in self.storage_latencies:
                    f.write(f"{latency}\n")
        elif inp == "2":
            dataset = input("Enter the dataset file path: ")
            code = input("Enter the code file path: ")
            weights = input("Enter the weights file path: ")
            self.initiate_tasks(code, dataset, weights)
        elif inp == "3":
            dataset = input("Enter the dataset file path: ")
            latency = self.measure_latency(self.compute, dataset)
            self.computation_latencies.append(latency)
            with open("compute_latencies.txt", "a") as f:
                for latency in self.computation_latencies:
                    f.write(f"{latency}\n")
            weights = input("Enter the directory to store weights: ")
            self.federated_averaging(weights, 1)
        elif inp == "4":
            self.plot_latencies()
        elif inp == "5":
            return

    def store_and_transmit_dataset(self, dataset):
        if self.get_storage_information(dataset):
            print(f"Dataset {dataset} already exists in storage.")
            return
        self.upload_dataset(dataset)
        self.initiate_data_distribution(self.data_locations, self.working_nodes)
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
            if status == communication_with_worker_pb2.IDLE:
                self.update_bootstrap(peer, "BUSY")
                result = self.compute_at_peer(peer)
                self.update_bootstrap(peer, "IDLE")

    def request_idle_workers(self):
        try:
            with grpc.insecure_channel(self.bootstrap_server_address) as channel:
                stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(
                    channel
                )
                response = stub.GetIdleWorkers(communication_with_bootstrap_pb2.Empty())
                idle_workers = [
                    address
                    for address in response.idle_workers
                    if address.IP != self.IP or address.port != self.port
                ]
                return idle_workers
        except grpc.RpcError as e:
            print(f"Error: Can not get Idle Workers - {e}")
            return 0

    def choose_workers(self, idle_workers):
        if len(idle_workers) == 0:
            print("No workers available. Try again later.")
            return []
        max_workers = int(os.getenv("UPPER_LIMIT_FOR_WORKERS", default=10))
        num_workers = min(len(idle_workers), max_workers)
        # Take user input or use a predetermined number of workers.
        required_workers = int(input("Enter the number of tasks to assign: "))
        if required_workers > num_workers:
            print(
                f"Number of tasks requested is greater than available workers. Assigning {num_workers} workers."
            )
            self.number_of_tasks = num_workers
        else:
            self.number_of_tasks = required_workers
        # Choose available workers for a task.
        # Filter out own address from the list of idle workers.
        chosen_workers = random.sample(idle_workers, self.number_of_tasks)
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
        donot_contact = []
        failed_peers = []
        for peer in peers:
            status = self.get_idle_ack(peer)
            if status == communication_with_worker_pb2.IDLE:
                self.update_bootstrap(peer, "BUSY")
                result = self.transmit_model_peer(codepath, peer, weights)
                if result == 0:
                    failed_peers.append(peer)
                    continue
                self.update_bootstrap(peer, "IDLE")
                donot_contact.append(peer)
            else:
                failed_peers.append(peer)

        if len(failed_peers) > 0:
            idle_peers = self.request_idle_workers()
            idle_peers = [(peer.IP, peer.port) for peer in idle_peers]
            idle_peers = [peer for peer in idle_peers if peer not in donot_contact]
            if len(idle_peers) == 0:
                print("No workers available. Try again later.")
                return

            if len(idle_peers) < len(failed_peers):
                print("Not enough workers available to transmit the code.")
                return

            if len(idle_peers) >= len(failed_peers):
                # from stroage see failed unit shard and send them to idle worker with code & weights
                for peer in failed_peers:
                    for unit in peers:
                        if unit[0] == peer[0] and unit[1] == peer[1]:
                            shard = unit[2]
                            path = (
                                datasetpath.split(".")[0]
                                + "shard"
                                + str(shard)
                                + "."
                                + datasetpath.split(".")[1]
                            )
                            for idle_peer in idle_peers:
                                status = self.get_idle_ack(idle_peer)
                                if status == communication_with_worker_pb2.IDLE:
                                    self.update_bootstrap(idle_peer, "BUSY")
                                    self.transmit_dataset_peer(
                                        (datasetpath, shard, path),
                                        idle_peer,
                                        datasetpath,
                                    )
                                    if result == 1:
                                        result = self.transmit_model_peer(
                                            codepath, idle_peer, weights
                                        )
                                        if result == 1:
                                            self.update_storage_information(
                                                datasetpath, 0
                                            )
                                            break
                                    self.update_bootstrap(idle_peer, "IDLE")

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

    def upload_dataset(self, dataset_path):
        # Upload dataset to bootstrap server or distribute to peers.
        directory_path = os.path.dirname(dataset_path)

        with open(dataset_path, "rb") as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]

        with open(dataset_path, mode="r", encoding=encoding) as file:
            csvreader = csv.reader(file)
            content = list(csvreader)

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
        left_over_tasks = []
        not_contacted_peers = []
        for peer in self.alloted_workers_to_shards.keys():
            for shard in self.alloted_workers_to_shards[peer]:
                status = self.get_idle_ack(peer)
                if status == communication_with_worker_pb2.IDLE:
                    self.update_bootstrap(peer, "BUSY")
                    result = self.transmit_dataset_peer(shard, peer, dataset_path)
                    if result == 0:
                        left_over_tasks.append(self.alloted_workers_to_shards[peer])
                        break
                    self.update_bootstrap(peer, "IDLE")
                else:
                    left_over_tasks.append(self.alloted_workers_to_shards[peer])
                    break
            not_contacted_peers.append(peer)

        if len(left_over_tasks) > 0:
            idle_peers = self.request_idle_workers()
            idle_peers = [(peer.IP, peer.port) for peer in idle_peers]
            idle_peers = [
                peer for peer in idle_peers if peer not in not_contacted_peers
            ]
            if len(idle_peers) == 0:
                print("No workers available. Try again later.")
                return

            if len(idle_peers) < len(left_over_tasks):
                print("Not enough workers available to transmit the dataset.")
                return

            if len(idle_peers) >= len(left_over_tasks):
                print(f"Left over tasks: {left_over_tasks}")
                print(f"not contacted peers: {not_contacted_peers}")
                print(f"Idle peers: {idle_peers}")
                for task in left_over_tasks:
                    for peer in idle_peers:
                        flag = 0
                        for shard in task:
                            status = self.get_idle_ack(peer)
                            if status == communication_with_worker_pb2.IDLE:
                                self.update_bootstrap(peer, "BUSY")
                                result = self.transmit_dataset_peer(
                                    shard, peer, dataset_path
                                )
                                if result == 0:
                                    flag = -1
                                    break
                                self.update_bootstrap(peer, "IDLE")
                            else:
                                flag = -1
                                break
                        if flag == 0:
                            idle_peers.remove(peer)
                            break

        update_status = 0
        while update_status == 0:
            update_status = self.update_storage_information(dataset_path, 0)
            print(f"Update status: {update_status}")

    def transmit_dataset_peer(self, data, peer, dataset_path):
        CHUNK_SIZE = int(4 * 1024 * 1024)
        with open(data[2], "r", newline="") as csvfile:
            dataset = list(csv.reader(csvfile))

        components = data[2].split("/")  # Split the path into components
        components[-2] = "compute"
        name, extention = components[-1].split(".")
        components[-1] = name.split("_")[0] + "." + extention
        filepath = "/".join(components)

        try:
            with grpc.insecure_channel(f"{peer[0]}:{peer[1]}") as channel:
                stub = communication_with_worker_pb2_grpc.WorkerServiceStub(channel)

                # Chunk the dataset and send each chunk
                total_rows = len(dataset)
                chunks = [
                    dataset[i : i + CHUNK_SIZE]
                    for i in range(0, total_rows, CHUNK_SIZE)
                ]

                for i, chunk in enumerate(chunks):
                    request = communication_with_worker_pb2.DatasetRequest(
                        datasetPath=filepath,
                        dataset=communication_with_worker_pb2.Dataset(
                            rows=[
                                communication_with_worker_pb2.Row(values=row)
                                for row in chunk
                            ]
                        ),
                    )
                    response = stub.DatasetTransfer(request)
                    print(
                        f"Chunk {i} transmitted to {peer} with status: {response.status}"
                    )

                    if response.status != "SUCCESS":
                        print(f"Failed to transmit chunk {i} to {peer}")
                        return 0

                if self.storageInformation.get(dataset_path):
                    self.storageInformation[dataset_path].append(peer + (data[1],))
                else:
                    self.storageInformation[dataset_path] = [peer + (data[1],)]
                print(f"Storage Information: {self.storageInformation}")
                return 1
        except grpc.RpcError as e:
            print(f"Failed to transmit dataset to {peer}: {e}")
            return 0

    def compute_at_peer(self, peer):
        try:
            with grpc.insecure_channel(f"{peer[0]}:{peer[1]}") as channel:
                stub = communication_with_worker_pb2_grpc.WorkerServiceStub(channel)
                request = communication_with_worker_pb2.ComputeRequest()
                response = stub.Compute(request)
                print(f"Computation completed at {peer} with status: {response.status}")
                if response.status == "SUCCESS":
                    # Create a directory called weights if not present.
                    if not os.path.exists("weights"):
                        os.makedirs("weights")

                    # Save the bytes received in response.chunk to a file called weights.joblib.
                    # For each peer append its address to the file name.
                    with open(f"weights/weights_{peer[0]}_{peer[1]}.joblib", "wb") as f:
                        f.write(response.chunk)
                    return 1
                return 0
        except grpc.RpcError as e:
            print(f"Failed to compute at {peer}: {e}")
            return 0

    def transmit_model_peer(self, filepath, peer, weights_filepath):
        try:
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
                        if model_response.status == "SUCCESS":
                            print("Path received:", model_response.modelPath)
                            print("Model transmission completed to peer:", peer)
                            return 1
                        else:
                            print("Model transmission failed.")
                            return 0
        except grpc.RpcError as e:
            print(f"Failed to transmit model to {peer}: {e}")
            return 0

    def get_idle_ack(self, peer):
        try:
            with grpc.insecure_channel(f"{peer[0]}:{peer[1]}") as channel:
                stub = communication_with_worker_pb2_grpc.WorkerServiceStub(channel)
                response = stub.IdleHeartbeat(
                    communication_with_worker_pb2.IdleHeartbeatRequest(message="Idle?")
                )
            return response.status
        except grpc.RpcError as e:
            print(f"Failed to get idle ack from {peer}: {e}")
            return "Inactive"

    def update_bootstrap(self, peer, state):
        try:
            with grpc.insecure_channel(self.bootstrap_server_address) as channel:
                stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(
                    channel
                )
                request = communication_with_bootstrap_pb2.UpdateIdleRequest(
                    address=communication_with_bootstrap_pb2.Address(
                        IP=peer[0], port=peer[1]
                    ),
                )
                if state == "IDLE":
                    stub.UpdateIdleWorker(request)
                elif state == "BUSY":
                    stub.UpdateNotIdleWorker(request)
        except grpc.RpcError as e:
            print(f"Failed to update status of {peer} because Bootstrap is down: {e}")

    def update_storage_information(self, dataset_path, type):
        try:
            with grpc.insecure_channel(self.bootstrap_server_address) as channel:
                stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(
                    channel
                )
                peers = []
                for peer in self.storageInformation[dataset_path]:
                    peers.append(
                        communication_with_bootstrap_pb2.Shards(
                            address=communication_with_bootstrap_pb2.Address(
                                IP=peer[0], port=peer[1]
                            ),
                            shard=peer[2],
                        )
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
                    request.type = (
                        communication_with_bootstrap_pb2.FileTypleEnum.DATASET
                    )
                else:
                    request.type = communication_with_bootstrap_pb2.FileTypleEnum.MODEL
                response = stub.UpdateStorage(request)
                print(f"Storage information updated with status: {response.status}")
                if response.status == "SUCCESS":
                    return 1
                return 0
        except grpc.RpcError as e:
            print(f"Failed to update storage information for {dataset_path}: {e}")
            return 0

    def get_storage_information(self, dataset_path):
        try:
            with grpc.insecure_channel(self.bootstrap_server_address) as channel:
                stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(
                    channel
                )
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
                    peers.append((peer.address.IP, peer.address.port))
                return peers
            return None
        except grpc.RpcError as e:
            print(f"Failed to get storage information for {dataset_path}: {e}")
            return None

    def plot_latencies(self):
        # Plot storage latencies
        plt.figure(figsize=(12, 6))
        with open("storage_latencies.txt", "r") as f:
            self.storage_latencies = [float(latency) for latency in f.readlines()]

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
        func(*args, **kwargs)
        end_time = time.time()
        latency = end_time - start_time
        return latency
