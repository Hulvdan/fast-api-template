from abc import ABC, abstractmethod


class IRandomRe(ABC):
    @abstractmethod
    def execute(self, re_pattern: str) -> str:
        raise NotImplementedError
