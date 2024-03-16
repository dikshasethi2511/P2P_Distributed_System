import grpc
import sys
sys.path.append('../proto')
sys.path.append('../classes')
import communication_with_bootstrap_pb2_grpc
from bootstrap_server import BootstrapServer
from concurrent import futures

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    communication_with_bootstrap_pb2_grpc.add_BootstrapServiceServicer_to_server(BootstrapServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()