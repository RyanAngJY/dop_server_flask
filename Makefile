DEP_PROTO_DIR=./proto/dep/proto

build:
	docker build -t ryanang/backend_server:latest .

start:
	make build
	docker run -p 8000:8000 ryanang/backend_server:latest

push:
	make build
	docker push ryanang/backend_server:latest

db:
 	# make sure you run `docker-compose up` first
	docker-compose exec db mysql -u root -proot -D test_db

gen: # Ryan TODO: By right, you are supposed to pull from the proto repository and compile instead of directly compiling from the source
	python -m grpc_tools.protoc -I$(DEP_PROTO_DIR) --python_out=proto/dep/python --grpc_python_out=proto/dep/python $(DEP_PROTO_DIR)/*/*.proto
