import itertools
from typing import Optional
import io

from .tokenizer import Tokenizer, Token, OPEN_BOLD, CLOSE_BOLD, OPEN_UNDERLINE, CLOSE_UNDERLINE, HEADLINE, CONTENT, \
    NEWLINE

import dominate
from dominate import tags


class Parser:
    """
    document  : (headline | paragraph | NEWLINE)* EOF;
    headline  : HEADLINE text_line;
    paragraph : expr (NEWLINE expr)* NEWLINE | EOF;
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

    def document(self):
        doc = dominate.document(title='Document')
        with doc:
            while self.tokens.current is not None:
                if (headline := self.headline()) is not None:
                    doc.add(headline)
                elif (paragraph := self.paragraph()) is not None:
                    doc.add(paragraph)
                elif self.tokens.current.type == NEWLINE:
                    next(self.tokens)
                else:
                    raise ValueError(f'Unexpected token: {self.tokens.current}')
        return doc


    def headline(self):
        if not self.tokens or self.tokens.current.type != HEADLINE:
            return None
        header = self.tokens.current
        next(self.tokens)
        headline_expr = self.text_line()
        level = header.value.count('#')
        tag = [tags.h1, tags.h2, tags.h3, tags.h4, tags.h5, tags.h6][level - 1]
        return tag(headline_expr)

    def paragraph(self):
        if (line := self.text_line()) is None:
            return None
        lines = [line]
        while self.tokens.current.type == NEWLINE:
            next(self.tokens)
            lines.append(self.text_line())


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
