import dataclasses
from abc import abstractmethod
from typing import Optional, Self


@dataclasses.dataclass
class Token:
    type: str
    start: int
    stop: int
    value: str

    def __eq__(self, other: str) -> bool:
        return self.type == other


class TokenizerRule:
    @classmethod
    @abstractmethod
    def tokenize(cls, code: str, current: int) -> Optional[Self]:
        ...
