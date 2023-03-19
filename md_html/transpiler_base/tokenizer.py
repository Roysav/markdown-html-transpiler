import dataclasses
import re
from abc import ABC, abstractmethod
from typing import Optional, Self, Type


@dataclasses.dataclass
class Token:
    type: str
    start: int
    stop: int
    value: str

    def __eq__(self, other: str) -> bool:
        return self.type == other


class TokenizerRule(ABC):
    @classmethod
    @abstractmethod
    def tokenize(cls, code: str, current: int) -> Optional[Token]:
        ...


class RegexRule(TokenizerRule):
    name: str

    @property
    @abstractmethod
    def match(self) -> str:
        ...

    @classmethod
    def tokenize(cls, code: str, current: int) -> Optional[Self]:
        if (match := re.match(cls.match, code[current:])) is not None:
            return Token(cls.name, current, current + match.end(), match.group())

    def __init_subclass__(cls, **kwargs):
        if not hasattr(cls, 'name'):
            cls.name = cls.__name__.upper()


class Tokenizer(ABC):
    @property
    @abstractmethod
    def rules(self) -> tuple[Type[TokenizerRule]]: ...

    def __init__(self, code: str):
        self.code = code
        self.index = 0
        self.current = next(self)


    def __bool__(self):
        return self.current is not None

    def peek(self) -> Optional[Token]:
        for rule in self.rules:
            if (token := rule.tokenize(self.code, self.index)) is not None:
                return token
        raise ValueError(f'No rule matched the code at index {self.index}')


    def __next__(self) -> Token:
        if self.index >= len(self.code):
            self.current = None
            return None
        next_ = self.peek()
        self.index = next_.stop
        self.current = next_
        return next_


    def __iter__(self):
        return self
