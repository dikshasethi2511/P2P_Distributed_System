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

    def request_idle_workers(self):
        with grpc.insecure_channel(self.bootstrap_server_address) as channel:
            stub = communication_with_bootstrap_pb2_grpc.BootstrapServiceStub(channel)
            try:
                response = stub.GetIdleWorkers(communication_with_bootstrap_pb2.Empty())
                max_workers = int(os.getenv("UPPER_LIMIT_FOR_WORKERS", default=10))
                num_workers = min(len(response.idle_workers), max_workers)
                # Take user input or use a predetermined number of workers.
                required_workers = int(input("Enter the number of tasks to assign: "))
                num_workers = min(num_workers, required_workers)
                self.leftover_count = required_workers - num_workers
                self.number_of_tasks = num_workers
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
        pass

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
