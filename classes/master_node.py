# The master node is the node that wants to initiate the task. It is responsible for choosing the workers, initiating the
# tasks, sending heartbeats to the working nodes, creating data shards, initiating data distribution, uploading, deleting,
# downloading, and updating the dataset, and adding tasks to the queue.

import grpc
import sys
import os
import random

sys.path.append("../proto")
import communication_with_bootstrap_pb2
import communication_with_bootstrap_pb2_grpc
from dotenv import load_dotenv

load_dotenv()
from task_queue import TaskQueue
import csv


class MasterNode:
    def __init__(self, bootstrap_server_address, IP, port, uuid):
        self.working_nodes = []
        self.number_of_tasks = 0
        self.leftover_count = 0
        self.task_queue = TaskQueue()
        self.data_locations = {}
        self.bootstrap_server_address = bootstrap_server_address
        self.IP = IP
        self.port = port
        self.uuid = uuid

    def run_master(self):
        # Run master node.
        self.request_idle_workers()
        print("Master Node Menu")
        print("1. Upload Dataset")
        inp = input("Enter your choice: ")
        if inp == "1":
            dataset = input("Enter the dataset directory path: ")
            self.upload_dataset(dataset)
            

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
                num_workers = min(num_workers, required_workers)
                self.leftover_count = required_workers - num_workers
                self.working_nodes = self.choose_workers(
                    num_workers, response.idle_workers
                )

            except grpc.RpcError as e:
                print(f"Error: gRPC communication failed - {e}")

    def choose_workers(self, num_workers, idle_workers):
        # Choose available workers for a task.
        # Filter out own address from the list of idle workers.
        idle_workers_chosen = [
            address
            for address in idle_workers
            if address.IP != self.IP or address.port != self.port
        ]
        chosen_workers = random.sample(idle_workers, num_workers)
        print(f"Chosen workers: {chosen_workers}")
        return chosen_workers

    def initiate_tasks(self, tasks):
        # Initiate tasks and distribute to chosen workers.
        pass

    def send_heart_beat(self):
        # Send heartbeat to working nodes.
        pass

    def create_shards(self, data):
        # Create data shards.
        pass

    def initiate_data_distribution(self, data, peers):
        # Distribute data to peers.
        pass

    def upload_dataset(self, dataset):
    # Upload dataset to bootstrap server or distribute to peers.
        dataset = "/mnt/c/Users/hp/Desktop/IIITD/BTP/P2P_Distributed_System/data"
        files = os.listdir(dataset)
        for file_name in files:
            file_path = os.path.join(dataset, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r', newline='') as csvfile:
                    csvreader = csv.reader(csvfile)
                    content = list(csvreader)  # Read CSV content into a list

                shard_size = len(content) // self.number_of_tasks
                remainder = len(content) % self.number_of_tasks

                # Create a directory for the file shards
                base_name, extension = os.path.splitext(file_name)
                file_shard_dir = os.path.join(dataset, f'{base_name}_shards')
                os.makedirs(file_shard_dir, exist_ok=True)

                # Divide the content into shards and store each shard in a separate file
                start = 0
                print(f"Shard size: {shard_size}")
                print(f"Number of tasks: {self.number_of_tasks}")
                for i in range(self.number_of_tasks):
                    # Adjust the shard size for the last shard if there is a remainder
                    size = shard_size + (1 if i < remainder else 0)
                    shard_content = content[start:start+size]
                    shard_file_path = os.path.join(file_shard_dir, f'{base_name}_shard_{i + 1}{extension}')
                    with open(shard_file_path, 'w', newline='') as shard_file:
                        shard_writer = csv.writer(shard_file)
                        shard_writer.writerows(shard_content)
                    start += size


    def delete_dataset(self, dataset):
        # Delete dataset.
        pass

    def download_dataset(self, dataset, peer):
        # Download dataset from bootstrap server or peer.
        pass

    def update_dataset(self, dataset, new_data):
        # Update dataset.
        pass

    def add_task_to_queue(self, task):
        # Add task to the queue.
        self.task_queue.enqueue(task)
        pass
