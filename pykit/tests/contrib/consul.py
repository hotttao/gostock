from urllib.parse import ParseResult
from pykit.registry import ServiceInstance
from pykit.contrib.registry.consul import ConsulClient
from pykit.contrib.registry.consul import ConsulImp


def test_consul_register():
    endpoints = [ParseResult(scheme='https', netloc='192.168.2.70:13304', 
                             path='', params='', query='', fragment='')]
    service = ServiceInstance(name='test', id='1', endpoints=endpoints, version='1.1')
    consul = ConsulClient(host='192.168.2.70', port=8500)
    consul.register(None, service)
    servers = consul.service(None, service='test', index=0, passing=False)
    print(servers)
    consul_imp = ConsulImp(client=consul)
    watcher, _ = consul_imp.watch(None, service_name='test')
    watcher.join()
