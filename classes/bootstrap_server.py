# The bootstrap server is responsible for managing the network of servers. It keeps track of the active and idle servers
# and their specifications. It also sends the list of active and idle servers to the requesting node. It also receives
# heartbeats from the servers and removes the server from the network if it does not receive a heartbeat from the server.
# The bootstrap server is not responsible for the actual computation of the tasks. It only manages the network of servers.
class BootstrapServer:
    def __init__(self):
        self.active_servers = []
        self.idle_servers = []
        self.server_specs = {}

    def add_server_to_network(self, server):
        # Add server to network.
        pass

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