import grpc
import sys
import os
from dotenv import load_dotenv

# Append the paths to sys.path
sys.path.append("../proto")
sys.path.append("../classes")

from peer import Peer
from threading import Thread, Event
from concurrent import futures


def run_peer(bootstrap_server_address):
    # Take input for the address and specs.
    CPU = '1' # input("Enter CPU: ")
    RAM = '2' # input("Enter RAM: ")
    storage = '3' # input("Enter storage: ")
    IP = input("Enter IP: ")
    port = input("Enter port: ")

    peer = Peer(bootstrap_server_address, IP, port)
    peer.connect_to_bootstrap_server(CPU, RAM, storage)


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Get the bootstrap server address from the environment variables
    bootstrap_server_address = os.getenv("BOOTSTRAP_SERVER_ADDRESS")

    if bootstrap_server_address is None:
        print("BOOTSTRAP_SERVER_ADDRESS is not set in the .env file")
        sys.exit(1)

    run_peer(bootstrap_server_address)
