# 服务器的证书过期更新
rm consul/certs/dc1-server-consul-0*
sudo docker run --rm -v $(pwd)/consul/certs:/certs --workdir /certs --entrypoint consul hashicorp/consul:1.11.2 tls cert create -server -dc dc1