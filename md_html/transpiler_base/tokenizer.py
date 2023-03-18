import dataclasses
from abc import abstractmethod
from typing import Optional, Self, Type


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


class Tokenizer:
    @property
    @abstractmethod
    def rules(self) -> tuple[Type[TokenizerRule]]: ...

    def __init__(self, code: str):
        self.code = code
        self.current = 0

    def __bool__(self):
        """
        :return: true if there is more code to tokenize
        """
        return self.current < len(self.code)

    def __next__(self):
        if not self:
            raise StopIteration

        for cls in self.rules:
            if token := cls.tokenize(self.code, self.current):
                return token
        raise SyntaxError(f'Unexpected token at {self.current}')
