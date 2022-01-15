from rstr import xeger  # type: ignore[import]

from ..interfaces.random_re import IRandomRe


class RandomReXeger(IRandomRe):
    def execute(self, re_pattern: str) -> str:
        return xeger(re_pattern)
