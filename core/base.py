from abc import ABC, abstractmethod

class BaseDbBackup(ABC):
    # @abstractmethod
    # def test_connection(self):
    #     pass

    @abstractmethod
    def backup(self):
        pass

    # @abstractmethod
    # def restore(self):
    #     pass
