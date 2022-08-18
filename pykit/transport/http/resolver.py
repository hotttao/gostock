
from typing import List
from pykit import context
from urllib.parse import urlparse
from urllib.parse import ParseResult
from pykit.selector import Selector, default_node
from pykit.registry import Discovery, ServiceInstance


class Resolver:

    def __init__(self, ctx: context.Context, discovery: Discovery, target: ParseResult,
                 selector: Selector, block: bool = False, insecure: bool = True):
        self.ctx = ctx
        self.target = target
        self.discovery = discovery
        self.selector = selector
        self.block = block
        self.insecure = insecure

        self.service_name = self.target.path.lstrip('/')
        self.watcher = self.discovery.watch(self.ctx, self.service_name, callback=self.update)

    def init(self, block: bool):
        if block:
            services, err = self.discovery.get_service(self.server_name)
            if not err:
                self.update(services)
            self.watcher.stop()

    def update(self, services: List[ServiceInstance]):
        print("run update......")
        nodes = []
        for ins in services:
            endpoints = ins.endpoints
            for endpoint in endpoints:
                end_obj = urlparse(endpoint)
                if not end_obj.netloc or end_obj.scheme != 'http':
                    continue
                node = default_node.DefaultNode.build("http", end_obj.netloc, ins)
                nodes.append(node)
                break
        if not nodes:
            print(f"[http resolver]Zero endpoint found,refused to write,set: {self.service_name} ins")
            return False

        self.selector.apply(nodes)
        return True

    def close(self):
        return self.watcher.stop()
