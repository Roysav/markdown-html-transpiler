import itertools
from typing import Optional
import io

from .tokenizer import Tokenizer, Token, OPEN_BOLD, CLOSE_BOLD, OPEN_UNDERLINE, CLOSE_UNDERLINE, HEADLINE, CONTENT, \
    NEWLINE

import dominate
from dominate import tags


class Parser:
    """
    paragraph : text_line+ NEWLINE;
    text_line : expr+ NEWLINE | EOF;
    expr      : bold | underline | content;
    bold      : OPEN_BOLD expr CLOSE_BOLD;
    underline : OPEN_UNDERLINE expr CLOSE_UNDERLINE;
    content   : CONTENT+;
    """
    def __init__(self, code: str):
        self.tokens = Tokenizer(code)

    def __bool__(self):
        return bool(self.tokens)

    def paragraph(self):
        if (line := self.text_line()) is None:
            return None
        lines = [line]
        while (line := self.text_line()) is not None:
            lines.append(line)
            if self.tokens and self.tokens.current.type == NEWLINE:
                next(self.tokens)
        return tags.p(*lines)

    def text_line(self):
        if (expr := self.expr()) is None:
            return None
        exprs = [expr]
        while (expr := self.expr()) is not None:
            exprs.append(expr)
        return tags.span(*exprs)

    def expr(self):
        for rule in self.expr_options():
            if (parsed := rule()) is not None:
                return parsed

    def bold(self):
        if self.tokens.current is None or self.tokens.current.type != OPEN_BOLD:
            return None
        next(self.tokens)
        inner = self.expr()
        if self.tokens.current.type == CLOSE_BOLD:
            next(self.tokens)
        return tags.b(inner)

    def underline(self):
        if self.tokens.current is None or self.tokens.current.type != OPEN_UNDERLINE:
            return None
        next(self.tokens)
        inner = self.expr()
        if self.tokens.current.type == CLOSE_UNDERLINE:
            next(self.tokens)
        return tags.u(inner)


    def content(self):
        if self.tokens.current is None or self.tokens.current.type != CONTENT:
            return None
        stream = io.StringIO()
        while self and self.tokens.current.type == CONTENT:
            stream.write(self.tokens.current.value)
            next(self.tokens)
        return tags.span(stream.getvalue())

    def expr_options(self):
        return [
            self.content,
            self.underline,
            self.bold,
        ]