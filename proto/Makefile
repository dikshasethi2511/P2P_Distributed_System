all:
	python3 -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. communication_with_bootstrap.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. communication_with_worker.proto

