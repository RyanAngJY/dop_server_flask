DEP_PROTO_DIR=./proto/dep
IMAGE_NAME=ryanang/backend_server:latest

build:
	docker build -t $(IMAGE_NAME) .

start:
	docker-compose down
	docker-compose up --build

dev_start:
	make start

push_to_docker_hub:
	make build
	docker push $(IMAGE_NAME)

db: # to access the DB shell
 	# make sure you run `docker-compose up` first
	docker-compose exec db mysql -u root -proot -D test_db

shell: # to enter the shell of the image
	make build
	docker run -it $(IMAGE_NAME) bash

health_check:
	curl http://localhost:8000/api/

# ========= Proto installation and generation ===========
install_proto_common:
	./proto/install_proto_common.sh

gen: # Ryan TODO: By right, you are supposed to pull from the proto repository and compile instead of directly compiling from the source
	python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. $(DEP_PROTO_DIR)/*/*.proto

install_gen:
	make install_proto_common
	make gen