DEP_PROTO_DIR=./proto/dep

build:
	docker build -t ryanang/backend_server:latest .

start:
	docker-compose up --build

dev_start:
	make start

bash:
	docker run --name dop_server_flask -p 8000:8000 ryanang/backend_server:latest
	docker exec dop_server_flask bash

push:
	make build
	docker push ryanang/backend_server:latest

db: # to access the DB shell
 	# make sure you run `docker-compose up` first
	docker-compose exec db mysql -u root -proot -D test_db

# ========= Proto installation and generation ===========
install_proto_common:
	./proto/install_proto_common.sh

gen: # Ryan TODO: By right, you are supposed to pull from the proto repository and compile instead of directly compiling from the source
	python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. $(DEP_PROTO_DIR)/*/*.proto

install_gen:
	make install_proto_common
	make gen