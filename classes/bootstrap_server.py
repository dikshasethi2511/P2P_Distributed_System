import sys
sys.path.append('../proto')
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

    def JoinNetwork(self, request, context):
        # Extract details from the JoinRequest.
        cpu = request.CPU
        ram = request.RAM
        storage = request.Storage

        # Store server specs in server_specs
        server_specs = {'CPU': cpu, 'RAM': ram, 'Storage': storage}
        self.server_specs[context.peer()] = server_specs

        # Add server to network
        self.add_server_to_network(context.peer())

        # Return existing peers
        existing_peers = [peer for peer in self.active_servers]
        response = communication_with_bootstrap_pb2.JoinResponse(existing_peers=existing_peers)
        return response

    def add_server_to_network(self, server):
        # Add server to active_servers list
        self.active_servers.append(server)

        # Add server to idle_servers list
        self.idle_servers.append(server)

    def send_idle_workers(self):
        # Send list of idle workers to requesting node.
        pass

    def send_active_workers(self):
        # Send list of active workers to requesting node.
        pass

    def send_heart_beat(self, server):
        # Receive heartbeats from servers.
        pass

    def remove_server(self, server):
        # Remove server from the network.
        pass