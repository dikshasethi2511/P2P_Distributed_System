import grpc
import sys
sys.path.append('../proto')
sys.path.append('../classes')
from peer import Peer
from concurrent import futures

def run_peer(bootstrap_server_address):
    peer = Peer(bootstrap_server_address)
    peer.connect_to_bootstrap_server()

if __name__ == "__main__":
    bootstrap_server_address = "localhost:50051"
    run_peer(bootstrap_server_address)
    