"""Реализация сервиса генерации случайных строк по паттерну регулярного выражения."""
from rstr import xeger  # type: ignore[import]

from common.services.random_re import IRandomRe


class RandomReXeger(IRandomRe):
    """Сервис генерации случайных строк по паттерну регулярного выражения.

    Использует rstr под капотом.
    """

    def execute(self, re_pattern: str) -> str:
        """Генерация случайной строки по паттерну регулярного выражения."""
        return xeger(re_pattern)
