from abc import ABCMeta, abstractmethod
from typing import Sequence

from docker.models.containers import Container
from docker.models.networks import Network
from yellowbox.containers import is_alive, _DEFAULT_TIMEOUT, get_aliases


class YellowService(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        return self

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def is_alive(self):
        pass

    @abstractmethod
    def connect(self, network: Network)->Sequence[str]:
        pass

    @abstractmethod
    def disconnect(self, network: Network):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False


class SingleContainerService(YellowService):
    def __init__(self, container: Container):
        self.container = container

    def connect(self, network: Network):
        network.connect(self.container)
        self.container.reload()
        return get_aliases(self.container, network)

    def disconnect(self, network: Network):
        network.disconnect(self.container)
        self.container.reload()

    def is_alive(self):
        return is_alive(self.container)

    def start(self):
        self.container.start()
        self.container.reload()
        return self  # For fluent interface, i.e. "with service.start():"

    def stop(self):
        if self.is_alive():
            self.container.kill()
            self.container.wait(timeout=_DEFAULT_TIMEOUT)
            self.container.reload()
