"""
This package contains Lexer class for lexing various tokens in expression.
"""

from __future__ import annotations
from typing import Iterator

from .token import Token
from .atomic_lexer import AtomicLexer
from .exceptions import IllegalCharacterError
from .lexers import lexers


# TODO - tested manually for few correct expressions manually

class Lexer:
    """Lexer object to tokenise the expression"""

    def __init__(self, expr: str, ignore_chars: tuple[str], atomic_lexers: tuple[AtomicLexer]):
        self.expr = expr
        self.ignore_chars = ignore_chars
        self.lexers = atomic_lexers

        self.pos = 0
        self.char = ''
        self.advance()

    def advance(self):
        """moves to next part of expression"""
        try:
            self.char = self.expr[self.pos]
            self.ignore()
        except IndexError:
            self.char = ''

    def ignore(self):
        """skips any char to be ignored"""
        while self.char in self.ignore_chars:
            self.pos += 1
            self.char = self.expr[self.pos]

    def illegal_char_error(self) -> IllegalCharacterError:
        """Creates exception object for illegal char"""
        return IllegalCharacterError(self.expr, self.pos)

    def next_token(self) -> Token:
        """tokenises expression one by one"""
        if self.pos >= len(self.expr):
            raise StopIteration

        while True:
            for cls_lexer in self.lexers:
                if cls_lexer.match(self.char):
                    lexer: AtomicLexer = cls_lexer(self.expr, self.pos)
                    tok = lexer.get_token()
                    self.pos = tok.end
                    self.advance()
                    return tok

            raise self.illegal_char_error()

    def __iter__(self) -> Lexer:
        return self

    __next__ = next_token


def lex(expr: str, ignore_chars: tuple[str] = (' ', '\t', '\n', '\r')) -> Iterator[Token]:
    """returns iterator of tokens"""
    return iter(
        Lexer(expr=expr, ignore_chars=ignore_chars, atomic_lexers=lexers)
    )
