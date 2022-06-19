
INTERNAL_PROTO_FILES=$(shell find crawler/internal -name *.proto)
API_PROTO_FILES=$(shell find api -name *.proto)

.PHONY: init
# init env
init:
	pip install grpcio
	pip install grpcio-tools
	pip install protoc-gen-swagger


.PHONY: config
# generate internal proto
config:
	protoc --proto_path=./ \
	       --proto_path=./third_party \
 	       --python_out=paths=source_relative:./ \
	       $(INTERNAL_PROTO_FILES)

.PHONY: api
# generate api proto
api:
	python -m grpc_tools.protoc \
		   --proto_path=./ \
	       --proto_path=./third_party \
 	       --python_out=./ \
 	       --grpc_python_out=./ \
 	       --openapi_out==paths=source_relative:. \
	       $(API_PROTO_FILES)

.PHONY: build
# build
build:


.PHONY: generate
# generate
generate:
	

.PHONY: all
# generate all
all:
	make api;
	make config;
	make generate;

# show help
help:
	@echo ''
	@echo 'Usage:'
	@echo ' make [target]'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
	helpMessage = match(lastLine, /^# (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 2, RLENGTH); \
			printf "\033[36m%-22s\033[0m %s\n", helpCommand,helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
