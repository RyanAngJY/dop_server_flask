DEP_PROTO_DIR=./proto/dep
IMAGE_NAME=ryanang/dop_server_flask:latest
CONSUMER_IMAGE_NAME=ryanang/dop_kafka_consumer:latest
.DEFAULT_GOAL := dev_start # set default target to run

# ============== Development ===============
# For development server
dev_start:
	make start

# For development server (on Docker)
start:
	docker-compose down
	docker-compose up --build

db: # to access the DB shell
 	# make sure you run `docker-compose up` first
	docker-compose exec db mysql -u root -proot -D test_db

build_local:
	docker build -t $(IMAGE_NAME) . -f Dockerfile.local

# Go into the shell of the Docker container
shell: build_local 
	# to enter the shell of the image
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

# ========= Building Docker Image ===========
build:
	docker build -t $(IMAGE_NAME) .
	docker build -t $(CONSUMER_IMAGE_NAME) . -f Dockerfile.consumer

# push to docker hub
push: build
	docker push $(IMAGE_NAME)
	docker push $(CONSUMER_IMAGE_NAME)
