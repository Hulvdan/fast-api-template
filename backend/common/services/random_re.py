"""Интерфейс сервиса генерации случайных строк по паттерну регулярного выражения."""
from abc import abstractmethod
from typing import Protocol


class IRandomRe(Protocol):
    """Интерфейс сервиса генерации случайных строк по паттерну регулярного выражения."""

    @abstractmethod
    def execute(self, re_pattern: str) -> str:
        """Генерация случайной строки по паттерну регулярного выражения."""
        raise NotImplementedError
