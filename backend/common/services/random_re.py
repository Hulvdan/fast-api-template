"""Интерфейс сервиса генерации случайных строк по паттерну регулярного выражения."""
from abc import ABC, abstractmethod


class IRandomRe(ABC):
    """Интерфейс сервиса генерации случайных строк по паттерну регулярного выражения."""

    @abstractmethod
    def execute(self, re_pattern: str) -> str:
        """Генерация случайной строки по паттерну регулярного выражения."""
        raise NotImplementedError
