import json
from abc import ABCMeta, abstractmethod
from typing import List, Tuple
from urllib import parse
from pykit import context
from pykit import errors


#  ServiceInstance is an instance of a service in a discovery system.
class ServiceInstance:
    def __init__(self, id: str, name: str, version: str, 
                 endpoints: List[parse.ParseResult], metadata: dict = None):
        #  ID is the unique instance ID as registered.
        # Name is the service name as registered.
        # Version is the version of the compiled.
        # Metadata is the kv pair metadata associated with the service instance.
        # Endpoints is endpoint addresses of the service instance.
        # schema:
        #   http:#127.0.0.1:8000?isSecure=false
        #   grpc:#127.0.0.1:9000?isSecure=false
        self.id = id
        self.name = name
        self.version = version
        self.endpoints = endpoints
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'endpoints': self.endpoints,
            'metadata': self.metadata
        }

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    __repr__ = __str__

# Watcher is service watcher.


class Watcher(metaclass=ABCMeta):
    # Next returns services in the following two cases:
    # 1.the first time to watch and the service instance list is not empty.
    # 2.any service instance changes found.
    # if the above two conditions are not met, it will block until context deadline exceeded or canceled
    @abstractmethod
    def next() -> Tuple[List[ServiceInstance], errors.Error]:
        pass

    # Stop close the watcher.
    @abstractmethod
    def stop() -> errors.Error:
        pass


class Registrar(metaclass=ABCMeta):
    #  Register the registration.
    @abstractmethod
    def register(ctx: context.Context, service: ServiceInstance) -> errors.Error:
        pass

    # Deregister the registration.
    @abstractmethod
    def deregister(ctx: context.Context, service: ServiceInstance) -> errors.Error:
        pass


# Discovery is service discovery.
class Discovery(metaclass=ABCMeta):
    # GetService return the service instances in memory according to the service name.
    @abstractmethod
    def get_service(ctx: context.Context, service_name: str) -> Tuple[List[ServiceInstance], errors.Error]:
        pass

    # Watch creates a watcher according to the service name.
    @abstractmethod
    def watch(ctx: context.Context, service_name: str) -> Tuple[Watcher, errors.Error]:
        pass
