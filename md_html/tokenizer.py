from typing import Optional, Self

from .transpiler_base import tokenizer

# token types
# ====================================================
from .transpiler_base.tokenizer import Token


OPEN_BOLD = 'OPEN_BOLD'
CLOSE_BOLD = 'CLOSE_BOLD'
OPEN_UNDERLINE = 'OPEN_UNDERLINE'
CLOSE_UNDERLINE = 'CLOSE_UNDERLINE'
HEADLINE = 'HEADLINE'
CONTENT = 'CONTENT'
NEWLINE = 'NEWLINE'


# ====================================================


class Bold(tokenizer.TokenizerRule):
    open = True

    @classmethod
    def tokenize(cls, code: str, current: int) -> Optional[Token]:
        if not code.startswith('**', current):
            return None

        token_type = OPEN_BOLD if cls.open else CLOSE_BOLD
        cls.open = not cls.open  # toggle cls.open
        return Token(token_type, current, current + 2, code[current:current + 2])


class Underline(tokenizer.TokenizerRule):
    open = True

    @classmethod
    def tokenize(cls, code: str, current: int) -> Optional[Token]:
        if not code.startswith('__', current):
            return None

        token_type = OPEN_UNDERLINE if cls.open else CLOSE_UNDERLINE
        cls.open = not cls.open
        return Token(token_type, current, current + 2, code[current:current + 2])


class Headline(tokenizer.RegexRule):
    r"""
    ^#{1,6}\s
    """
    match = r'#{1,6}\s'

    @classmethod
    def tokenize(cls, code: str, current: int) -> Optional[Token]:
        if current == 0 or code[current - 1] == '\n':  # if it's the start of a new line or the start of the file
            return super().tokenize(code, current)


class Newline(tokenizer.RegexRule):
    match = r'\n'


class Content(tokenizer.RegexRule):
    match = r'.'


class Tokenizer(tokenizer.Tokenizer):
    rules = [
        Bold,
        Underline,
        Headline,
        Newline,
        Content,
    ]
