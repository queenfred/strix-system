
from abc import ABC, abstractmethod

class IUnitOfWork(ABC):
    @abstractmethod
    def __enter__(self): pass

    @abstractmethod
    def __exit__(self, *args): pass

    @abstractmethod
    def commit(self): pass

    @abstractmethod
    def rollback(self): pass
