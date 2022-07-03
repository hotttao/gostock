#!/usr/bin/env bash

set -e
SHELL_PATH=`readlink -f $0`
ROOT=$(dirname  $SHELL_PATH)

docker-compose -f $ROOT/mysql/docker-compose.yaml down
docker-compose -f $ROOT/redis/docker-compose.yaml down
docker-compose -f $ROOT/jaeper/jaeper-hotrod.yaml down
docker-compose -f $ROOT/tig/docker-compose.yaml down
docker-compose -f $ROOT/consul/docker-compose.yaml down