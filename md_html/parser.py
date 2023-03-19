import itertools
from typing import Optional
import io

from .tokenizer import Tokenizer, Token, OPEN_BOLD, CLOSE_BOLD, OPEN_UNDERLINE, CLOSE_UNDERLINE, HEADLINE, CONTENT, \
    NEWLINE

import dominate
from dominate import tags


class Parser:
    """
    Parses a markdown file and returns the HTML code

    grammar:
    --------
    document: (headline | paragraph)*;
    paragraph : (expr)+ (NEWLINE | EOF);
    headline: HEADLINE expr (NEWLINE | EOF);
    expr : bold | underline | content;
    bold: OPEN_BOLD expr CLOSE_BOLD;
    underline: OPEN_UNDERLINE expr CLOSE_UNDERLINE;
    content: CONTENT+;
    """

    def __bool__(self):
        return bool(self.tokens)

    def __init__(self, code: str):
        self.tokens = Tokenizer(code)

    def document(self):
        doc = dominate.document()
        while self:
            for option in (self.headline, self.paragraph):
                result = option()
                if result is not None:
                    doc.add(result)
                    break
        return doc

    def paragraph(self):
        tag = tags.p()
        if (expr := self.expr()) is None:
            return None
        tag.add(expr)
        while (expr := self.expr()) is not None:
            tag.add(expr)
        if self and self.tokens.current.type == NEWLINE:
            next(self.tokens)
        return tag

    def expr(self):
        for option in self.expr_options():
            result = option()
            if result is not None:
                return result

    def headline(self) -> Optional[tags.h1 | tags.h2 | tags.h3 | tags.h4 | tags.h5 | tags.h6]:
        if self.tokens.current.type != HEADLINE:
            return None
        level = self.tokens.current.value.count('#')
        next(self.tokens)
        inner = self.expr()
        if self.tokens.current is not None and self.tokens.current.type != NEWLINE:
            raise ValueError("Expected newline after headline")
        next(self.tokens)
        level_tag = [tags.h1, tags.h2, tags.h3, tags.h4, tags.h5, tags.h6][level - 1]
        return level_tag(inner)


    def bold(self) -> Optional[tags.b]:
        if not self or self.tokens.current.type != OPEN_BOLD:
            return None
        next(self.tokens)
        inner = self.expr()
        if self.tokens.current.type != CLOSE_BOLD:
            raise ValueError("Expected closing bold tag")
        next(self.tokens)
        return tags.b(inner)

    def underline(self) -> Optional[tags.u]:
        if not self or self.tokens.current.type != OPEN_UNDERLINE:
            return None
        next(self.tokens)
        inner = self.expr()
        if self.tokens.current.type != CLOSE_UNDERLINE:
            raise ValueError("Expected closing underline tag")
        next(self.tokens)
        return tags.u(inner)

    def content(self) -> Optional[tags.span]:
        if not self or self.tokens.current.type != CONTENT:
            return None
        inner = io.StringIO()
        while self and self.tokens.current.type == CONTENT:
            inner.write(self.tokens.current.value)
            next(self.tokens)

        return tags.span(inner.getvalue())

    def expr_options(self):
        return self.content, self.bold, self.underline

