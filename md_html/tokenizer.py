from typing import Optional, Self

from .transpiler_base import tokenizer


# token types
# ====================================================
OPEN_BOLD = 'OPEN_BOLD'
CLOSE_BOLD = 'CLOSE_BOLD'
OPEN_UNDERLINE = 'OPEN_UNDERLINE'
CLOSE_UNDERLINE = 'CLOSE_UNDERLINE'
HEADLINE = 'HEADLINE'
CONTENT = 'CONTENT'


# ====================================================


class Bold(tokenizer.TokenizerRule):
    open = True

    @classmethod
    def tokenize(cls, code: str, current: int) -> Optional[tokenizer.Token]:
        if not code.startswith('**'):
            return None

        token_type = OPEN_BOLD if cls.open else CLOSE_BOLD
        cls.open = not cls.open  # toggle cls.open
        return tokenizer.Token(token_type, current, current + 2, '**')


class Underline(tokenizer.TokenizerRule):
    open = True

    @classmethod
    def tokenize(cls, code: str, current: int) -> Optional[tokenizer.Token]:
        if not code.startswith('__'):
            return None

        token_type = OPEN_UNDERLINE if cls.open else CLOSE_UNDERLINE
        cls.open = not cls.open
        return tokenizer.Token(token_type, current, current + 2, '__')


class Headline(tokenizer.RegexRule):
    """
    ^#{1,6}\s
    """
    match = r'#{1,6}\s'

    @classmethod
    def tokenize(cls, code: str, current: int) -> Optional[tokenizer.Token]:
        if current == 0 or code[current - 1] == '\n':  # if it's the start of a new line or the start of the file
            return super().tokenize(code, current)
