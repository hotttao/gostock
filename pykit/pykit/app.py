import os
import copy
import signal
from typing import List
from urllib.parse import ParseResult
import multiprocessing as mp
from pykit.context import Context
from pykit.registry import Registrar, ServiceInstance
from pykit.transport import IServer


SIGNAL_TRANSLATION_MAP = {
    signal.SIGINT: 'SIGINT',
    signal.SIGTERM: 'SIGTERM',
}


class DelayedKeyboardInterrupt:
    def __init__(self, propagate_to_forked_processes=None):
        """
        Constructs a context manager that suppresses SIGINT & SIGTERM signal handlers
        for a block of code.
        The signal handlers are called on exit from the block.
        Inspired by: https://stackoverflow.com/a/21919644
        :param propagate_to_forked_processes: This parameter controls behavior of this context manager
        in forked processes.
        If True, this context manager behaves the same way in forked processes as in parent process.
        If False, signals received in forked processes are handled by the original signal handler.
        If None, signals received in forked processes are ignored (default).
        """
        self._pid = os.getpid()
        self._propagate_to_forked_processes = propagate_to_forked_processes
        self._sig = None
        self._frame = None
        self._old_signal_handler_map = None

    def __enter__(self):
        self._old_signal_handler_map = {
            sig: signal.signal(sig, self._handler)
            for sig, _ in SIGNAL_TRANSLATION_MAP.items()
        }

    def __exit__(self, exc_type, exc_val, exc_tb):
        for sig, handler in self._old_signal_handler_map.items():
            signal.signal(sig, handler)

        if self._sig is None:
            return

        self._old_signal_handler_map[self._sig](self._sig, self._frame)

    def _handler(self, sig, frame):
        self._sig = sig
        self._frame = frame

        #
        # Protection against fork.
        #
        if os.getpid() != self._pid:
            if self._propagate_to_forked_processes is False:
                print(f'!!! DelayedKeyboardInterrupt._handler: {SIGNAL_TRANSLATION_MAP[sig]} received; '
                      f'PID mismatch: {os.getpid()=}, {self._pid=}, calling original handler')
                self._old_signal_handler_map[self._sig](self._sig, self._frame)
            elif self._propagate_to_forked_processes is None:
                print(f'!!! DelayedKeyboardInterrupt._handler: {SIGNAL_TRANSLATION_MAP[sig]} received; '
                      f'PID mismatch: {os.getpid()=}, ignoring the signal')
                return
            # elif self._propagate_to_forked_processes is True:
            #   ... passthrough

        print((f'!!! DelayedKeyboardInterrupt._handler: {SIGNAL_TRANSLATION_MAP[sig]}'
               f'received; delaying KeyboardInterrupt'))


class PyKit:
    def __init__(self, id: str, name: str, version: str,
                 servers: List[IServer], registry_timeout: int = 60,
                 metadata: dict = None, stop_timeout: int = 60,
                 endpoints: List[ParseResult] = None, registrar: Registrar=None):
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
        self.metadata = metadata or {}
        self.endpoints = endpoints or []

        self.registrar = registrar
        self.registry_timeout = registry_timeout
        self.stop_timeout = stop_timeout
        self.servers = servers

        self.stop_event = mp.Event()
        self.ctx = Context(stop_event=self.stop_event)
        self.instance = None
        self.process = []

    def start_server_process(self, server: IServer):
        def _process_worker(server):
            try:
                with DelayedKeyboardInterrupt():
                    server.start()
            except KeyboardInterrupt:
                print('server: got KeyboardInterrupt will exit')

        process = mp.Process(target=_process_worker, args=(server,))
        process.start()
        self.process.append(process)

    def run(self):
        """启动服务
        """
        try:
            self.start()
            self.stop_event.wait()
        except KeyboardInterrupt:
            try:
                with DelayedKeyboardInterrupt():
                    self.stop()
            except KeyboardInterrupt:
                print('Application.run: got KeyboardInterrupt during stop')

    def start(self):
        self.instance = self.build_instances()
        for s in self.servers:
            self.start_server_process(s)
        if self.registrar:
            print('registrar')
            print(self.instance)
            self.registrar.register(self.ctx, self.instance)

    def stop(self):
        instance = self.instance
        if self.registrar and self.instance:
            self.registrar.deregister(self.ctx, instance)
        for s in self.servers:
            s.stop()
        for p in self.process:
            p.join()

    def build_instances(self):
        endpoints = copy.deepcopy(self.endpoints)
        if not endpoints:
            for s in self.servers:
                endpoints.append(s.endpoint)
        instances = ServiceInstance(
            id=self.id, name=self.name, version=self.version,
            endpoints=endpoints,
            metadata=self.metadata
        )
        print(instances)
        return instances
