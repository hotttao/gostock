
from urllib.parse import urlparse
import consul
from typing import List, Tuple, Dict
from pykit import error
from pykit import context

from pykit.registry import Registrar, Discovery
from pykit.registry import ServiceInstance, Watcher
from pykit.registry.watcher import BaseThread


class ConsulClient:
    def __init__(self, host, port, scheme, verify=True):
        self.client = consul.Consul(host, port, scheme, verify=verify)

    def resolve(self, ctx: context.Context, nodes: List[Dict]) -> List[ServiceInstance]:
        """将 consule 保存的结果解析为 ServiceInstance

        Returns:
            List[ServiceInstance]: _description_
        """
        instances = []
        for node in nodes:
            i = ServiceInstance(id=node['ID'], name=node['Node'], version=node['Version'],
                                metadata=node['Metadata'], endpoint=node['Endpoints'])
            instances.append(i)
        return instances

    def service(self, ctx: context.Context, service: str, index: int,
                passing: bool) -> Tuple[List[ServiceInstance], int, error.Error]:
        index, nodes = self.client.health.service(service=service, passing=passing, index=index, wait=55)
        return self.resolver(ctx, nodes), index, None

    def deregister(self, ctx: context.Context, service: ServiceInstance) -> error.Error:
        self.client.agent.service.deregister(service_id=service.id)

    def register(self, ctx: context.Context, service: ServiceInstance) -> error.Error:
        endpoints = service.endpoints
        if endpoints:
            endpoint = endpoints[0]
            host_info = urlparse(endpoint)
            check = consul.Check.tcp(host_info.hostname, host_info.port, "5s", "30s", "30s")
            self.client.agent.service.register(name=service.name,
                                               service_id=service.id,
                                               address=host_info.hostname,
                                               port=host_info.port,
                                               check=check)
        return None


class ConsulImp(Registrar, Discovery):
    def deregister(self, ctx: context.Context, service: ServiceInstance) -> error.Error:
        pass

    def register(self, ctx: context.Context, service: ServiceInstance) -> error.Error:
        return super().register(service)

    def get_service(self, ctx: context.Context,
                    service_name: str) -> Tuple[List[ServiceInstance], error.Error]:
        # poll a key for updates
        index = None
        index, data = self.client.kv.get(self.endpoint, index=index)
        print(data['Value'])

    def watch(ctx: context.Context, service_name: str) -> Tuple[Watcher, error.Error]:
        return super().watch(service_name)


class ConsulWatcher(BaseThread):
    def __init__(self,):
        pass

    def run(self):
        pass
