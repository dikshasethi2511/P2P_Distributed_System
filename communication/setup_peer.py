import grpc
import sys

sys.path.append("../proto")
sys.path.append("../classes")
from peer import Peer
from threading import Thread, Event
from concurrent import futures
from dotenv import load_dotenv


def run_peer(bootstrap_server_address):
    # Take input for the address and specs.
    CPU = input("Enter CPU: ")
    RAM = input("Enter RAM: ")
    storage = input("Enter storage: ")
    IP = input("Enter IP: ")
    port = input("Enter port: ")

    peer = Peer(bootstrap_server_address, IP, port)
    peer.connect_to_bootstrap_server(CPU, RAM, storage)



if __name__ == "__main__":
    bootstrap_server_address = "localhost:50051"
    run_peer(bootstrap_server_address)
