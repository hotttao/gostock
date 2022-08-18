import copy
import json
import threading
import consul
from typing import List, Tuple, Dict

from pykit import errors
from pykit import context

from pykit.registry import Registrar, Discovery
from pykit.registry import ServiceInstance, Watcher
from pykit.registry.watcher import BaseThread


class ConsulClient:
    def __init__(self, host='127.0.0.1',
                 port=8500,
                 token=None):
        self.client = consul.Consul(host, port, token=token)

    def resolve(self, ctx: context.Context, nodes: List[Dict]) -> List[ServiceInstance]:
        """将 consule 保存的结果解析为 ServiceInstance

        Returns:
            List[ServiceInstance]: _description_
        """
        instances = []
        for node in nodes:
            # print(json.dumps(node, indent=4))
            service = node['Service']
            endpoint = f"http://{service['Address']}:{service['Port']}"
            version = ''
            for i in service['Tags']:
                tag = i.split('=', 1)
                if len(tag) == 2 and tag[0] == 'version':
                    version = tag[1]

            i = ServiceInstance(id=service['ID'], name=service['Service'], version=version,
                                metadata=service['Meta'], endpoints=[endpoint])
            instances.append(i)
        return instances

    def service(self, ctx: context.Context, service: str, index: int = 0,
                passing: bool = True) -> Tuple[List[ServiceInstance], int, errors.Error]:
        index, nodes = self.client.health.service(service=service, passing=passing, index=index, wait=55)
        # index, nodes = self.client.catalog.service(service=service, passing=passing, index=index, wait=55)
        return self.resolve(ctx, nodes), index, None

    def deregister(self, ctx: context.Context, service: ServiceInstance) -> errors.Error:
        self.client.agent.service.deregister(service_id=service.id)

    def register(self, ctx: context.Context, service: ServiceInstance) -> errors.Error:
        endpoints = service.endpoints
        if endpoints:
            for host_info in endpoints:
                check = consul.Check.tcp(host_info.hostname, host_info.port, "5s", "30s", "30s")
                self.client.agent.service.register(name=service.name,
                                                   service_id=service.id,
                                                   address=host_info.hostname,
                                                   port=host_info.port,
                                                   tags=[f'version={service.version}'],
                                                   check=check)
        return None


class ConsulImp(Registrar, Discovery):
    def __init__(self, client: ConsulClient):
        self.client = client
        self.watched_services = {}
        self.lock = threading.Lock()

    def deregister(self, ctx: context.Context, service: ServiceInstance) -> errors.Error:
        return self.client.deregister(ctx, service)

    def register(self, ctx: context.Context, service: ServiceInstance) -> errors.Error:
        return self.client.register(ctx, service)

    def get_service(self, ctx: context.Context,
                    service_name: str) -> Tuple[List[ServiceInstance], errors.Error]:
        with self.lock:
            server_set = self.watched_services.get(service_name, None)
            if server_set:
                instances = copy.deepcopy(server_set.instances)
                return instances, None
        return [], None

    def watch(self, ctx: context.Context, service_name: str, callback=None) -> Watcher:
        with self.lock:
            if service_name not in self.watched_services:
                instances, last_index, err = self.client.service(ctx, service_name)
                print("init instance: %s" % instances)
                server_set = ServerSet(service_name=service_name, service_instances=instances, 
                                       callback=callback)
                self.watched_services[service_name] = server_set
            server_set = self.watched_services[service_name]
            watcher = ConsulWatcher(service_set=server_set, imp=self)
            watcher.start()
            return watcher, None


class ServerSet:
    def __init__(self, service_name: str, service_instances: List[ServiceInstance],
                 callback=None) -> None:
        self.service_name = service_name
        self.service_instances = service_instances
        self.lock = threading.Lock()
        self.callback = callback

        if self.callback:
            self.callback(self.service_instances)

    @property
    def instances(self):
        with self.lock:
            return self.service_instances

    def update_instance(self, service_instances: List[ServiceInstance]):
        with self.lock:
            self.service_instances = service_instances
            if self.callback:
                self.callback(self.service_instances)


class ConsulWatcher(BaseThread):
    def __init__(self, service_set: ServerSet, imp: ConsulImp):
        self.service_set = service_set
        self.imp = imp
        super(ConsulWatcher, self).__init__()

    def run(self):
        last_index = 0
        while True:
            if self.stopped_event.wait(timeout=1):
                return
            print('consule watcher running')
            s = self.imp.client.service(None, service=self.service_set.service_name)
            instances, tmp_index, error = s
            # print(json.dumps(instances, indent=4))
            if tmp_index != last_index and tmp_index != 0:
                print('update instances')
                self.service_set.update_instance(instances)
                last_index = tmp_index
