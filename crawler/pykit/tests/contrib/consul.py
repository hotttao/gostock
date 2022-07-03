from pykit.registry import ServiceInstance
from pykit.contrib.registry.consul import ConsulClient


def test_consul_register():
    service = ServiceInstance(name='test', id='1', endpoints=['https://192.168.2.70:13304'], version='1.1')
    consul = ConsulClient(host='192.168.2.70', port=8500)
    consul.register(None, service)
    servers = consul.service(None, service='test', index=0, passing=False)
    print(servers)
