
import signal
from typing import List
from urllib.parse import ParseResult
from pykit.context import Context
from pykit.registry import Registrar
from pykit.transport import Server


class PyKit:
    def __init__(self, id: str, name: str, version: str, metadata: dict, endpoints: List[ParseResult],
                 ctx: Context, sigs: List[signal.Signals], registrar: Registrar,
                 registry_timeout: int, stop_timeout: int, servers: Server):
        """_summary_

        Args:
            id (str): _description_
            name (str): _description_
            version (str): _description_
            metadata (dict): _description_
            endpoints (List[ParseResult]): _description_
            ctx (Context): _description_
            sigs (List[signal.Signals]): _description_
            registrar (Registrar): _description_
            registry_timeout (int): _description_
            stop_timeout (int): _description_
            servers (Server): _description_
        """
        self.id = id
        self.name = name
        self.version = version
        self.metadata = metadata
        self.endpoints = endpoints
        self.ctx = ctx
        self.sigs = sigs
        self.registrar = registrar
        self.registry_timeout = registry_timeout
        self.stop_timeout = stop_timeout
        self.servers = servers
