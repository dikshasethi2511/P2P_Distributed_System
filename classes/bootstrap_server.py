import sys
import uuid
import time
from threading import Lock, Thread

sys.path.append("../proto")
import communication_with_bootstrap_pb2
import communication_with_bootstrap_pb2_grpc


# The bootstrap server is responsible for managing the network of servers. It keeps track of the active and idle servers
# and their specifications. It also sends the list of active and idle servers to the requesting node. It also receives
# heartbeats from the servers and removes the server from the network if it does not receive a heartbeat from the server.
# The bootstrap server is not responsible for the actual computation of the tasks. It only manages the network of servers.
class BootstrapServer(communication_with_bootstrap_pb2_grpc.BootstrapServiceServicer):
    def __init__(self):
        self.active_servers = []
        self.idle_servers = []
        self.server_specs = {}
        self.servers = {}
        self.active_heartbeat = {}
        self.heartbeat_lock = Lock()
        self.check_heartbeat_thread = Thread(target=self.check_heartbeat, args=())
        self.check_heartbeat_thread.start()
        self.storageInformation = {}

    def JoinNetwork(self, request, context):
        # Extract details from the JoinRequest.
        IP = request.address.IP
        port = request.address.port
        cpu = request.specs.CPU
        ram = request.specs.RAM
        storage = request.specs.storage

        # Store server specs in server_specs.
        server_specs = {"CPU": cpu, "RAM": ram, "Storage": storage}
        if (IP, port) not in self.server_specs:
            self.server_specs[(IP, port)] = server_specs
            peer_uuid = str(uuid.uuid1())
            # Add server to servers list.
            self.servers[peer_uuid] = (IP, port)

            # Add server to network.
            self.add_server_to_network(peer_uuid)
            existing_peers = self.send_active_workers()
        else:
            peer_uuid = None
            existing_peers = []

        response = communication_with_bootstrap_pb2.JoinResponse(
            uuid=peer_uuid, existing_peers=existing_peers
        )
        return response

    def ActiveHeartbeat(self, request, context):
        # Extract details from the HeartbeatRequest.
        peer_uuid = request.uuid
        status = "FAILURE"
        # Update the heartbeat of the server.
        if self.update_heartbeat(peer_uuid):
            status = "SUCCESS"

        # Return status of the heartbeat.
        return communication_with_bootstrap_pb2.HeartbeatResponse(status=status)

    def GetIdleWorkers(self, request, context):
        # Return list of idle workers.
        response = communication_with_bootstrap_pb2.IdleWorkersResponse(
            idle_workers=self.send_idle_workers()
        )
        return response

    def UpdateNotIdleWorker(self, request, context):
        peer_ip = request.address.IP
        peer_port = request.address.port
        for peer in self.servers:
            if self.servers[peer] == (peer_ip, peer_port):
                peer_uuid = peer
                break

        if peer_uuid in self.idle_servers:
            self.idle_servers.remove(peer_uuid)

        return communication_with_bootstrap_pb2.Empty()

    def UpdateIdleWorker(self, request, context):
        peer_ip = request.address.IP
        peer_port = request.address.port
        for peer in self.servers:
            if self.servers[peer] == (peer_ip, peer_port):
                peer_uuid = peer
                break

        if peer_uuid not in self.idle_servers:
            self.idle_servers.append(peer_uuid)

        return communication_with_bootstrap_pb2.Empty()

    def UpdateStorage(self, request, context):
        master = (request.address.IP, request.address.port)
        if master not in self.storageInformation.keys():
            self.storageInformation[master] = {}

        if request.path not in self.storageInformation[master].keys():
            self.storageInformation[master][request.path] = {}
            self.storageInformation[master][request.path]["type"] = (
                "dataset" if request.type == 0 else "model"
            )
            self.storageInformation[master][request.path]["peers"] = []

            for peer in request.workers:
                print(peer)
                self.storageInformation[master][request.path]["peers"].append(
                    (peer.address.IP, peer.address.port, peer.shard)
                )
        else:
            for peer in request.workers:
                for peerbefore in self.storageInformation[master][request.path]["peers"]:
                    if peer.shard == peerbefore[2]:
                        self.storageInformation[master][request.path]["peers"].remove(
                            peerbefore
                        )
                        self.storageInformation[master][request.path]["peers"].append(
                            (peer.address.IP, peer.address.port, peer.shard)
                        )
            self.storageInformation

        print(self.storageInformation)
        return communication_with_bootstrap_pb2.UpdateStorageResponse(status="SUCCESS")
    def GetStorage(self, request, context):
        master = (request.address.IP, request.address.port)
        path = request.path
        if master in self.storageInformation.keys():
            if path in self.storageInformation[master].keys():
                peers = []
                for peer in self.storageInformation[master][path]["peers"]:
                    peers.append(
                        communication_with_bootstrap_pb2.Shards(
                            address=communication_with_bootstrap_pb2.Address(
                                IP=peer[0], port=peer[1]
                            ),
                            shard=peer[2],
                        )
                    )
                print(peers)
                return communication_with_bootstrap_pb2.GetStorageResponse(
                    status="SUCCESS", workers=peers
                )

        return communication_with_bootstrap_pb2.GetStorageResponse(
            status="FAILURE", workers=[]
        )

    def add_server_to_network(self, peer_uuid):
        # Add server to active_servers list.
        self.active_servers.append(peer_uuid)
        # Add server to idle_servers list.
        self.idle_servers.append(peer_uuid)
        # Add server to HeartBeatTracker.
        self.active_heartbeat[peer_uuid] = time.time()

    def update_heartbeat(self, uuid):
        if uuid not in self.active_heartbeat.keys():
            return 0
        self.active_heartbeat[uuid] = time.time()
        if uuid not in self.active_servers:
            self.active_servers.append(uuid)
        return 1

    def send_idle_workers(self):
        # Send list of idle workers to requesting node.
        return [
            communication_with_bootstrap_pb2.Address(
                IP=self.servers[peer][0], port=self.servers[peer][1]
            )
            for peer in self.idle_servers
        ]

    def send_active_workers(self):
        # Send list of active workers to requesting node.
        return [
            communication_with_bootstrap_pb2.Address(
                IP=self.servers[peer][0], port=self.servers[peer][1]
            )
            for peer in self.active_servers
        ]

    def remove_server(self, uuid):
        # Remove server from the network.
        if uuid in self.active_servers:
            self.active_servers.remove(uuid)
            self.idle_servers.remove(uuid)
            self.server_specs.pop(self.servers[uuid])
            self.servers.pop(uuid)
            print(f"Server {uuid} has been removed from the network due to inactivity.")

    def check_heartbeat(self):
        while True:
            with self.heartbeat_lock:
                peers = self.active_servers

            for uuid in peers:
                if time.time() - self.active_heartbeat[uuid] > 18:
                    self.remove_server(uuid)
