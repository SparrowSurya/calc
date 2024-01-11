"""
Module: calc.lexer
Description: Provides the classes & functions to tokenise the expression.

Usage:
>>> l = Lexer('2+3', ignore=[' ', '\t'])
>>> l.tokenise()
(Token(NUMBER, '2', 0:1), Token(PLUS, '+', 1:2), Token(NUMBER, '3', 2:3))
>>> [token for token in lex('2+3')]
[Token(NUMBER, '2', 0:1), Token(PLUS, '+', 1:2), Token(NUMBER, '3', 2:3)]
"""

from __future__ import annotations
from typing import Iterable, Iterator

from .token import Token
from .unit_lexer import UnitLexer, default as default_lexers
from .exceptions import IllegalCharError


__all__ = (
    "Lexer",
    "lex",
)


class Lexer:
    """A Lexer object to tokenise the expression.

    The lexer makes use of collection of unit lexers to tokenise different elements in the
    expression. The lexer is a simple implementation trying to tokenise the expression
    starting from given index.
    """

    def __init__(self, expr: str, ignore: str, lexers: Iterable[type[UnitLexer]]):
        """
        Arguments:
        - expr: expression to tokenise.
        - ignore: characters to ignore while tokenising, for e.g. whitespace.
        - lexers: unit lexers to be used to tokenise the expression.
        """
        self.expr = expr
        self.ignore_chars = ignore
        self.lexers = lexers

        self.pos = 0
        self.char: str | None = None
        self.advance()

    def advance(self):
        """Moves to next character of expression.

        NOTE: Sets the character to `None` if reached end of expression.
        """
        try:
            self.char = self.expr[self.pos]
            self.skip_chars()
        except IndexError:
            self.char = None

    def skip_chars(self):
        """Skips the characters to be ignored."""
        while self.char and self.char in self.ignore_chars:
            self.pos += 1
            self.char = self.expr[self.pos]

    def illegal_char_error(self) -> IllegalCharError:
        """Provides the error class when none of lexers matches the part."""
        msg = f"illegal character '{self.char}' found at index {self.pos} during lexing"
        return IllegalCharError(self.expr, self.pos, msg)

    def next_token(self) -> Token:
        """Provides one token at a time.

        Raises:
        - IllegalCharError: when a char is not accepted by any lexer & not in ignore chars.
        - StopIteration: reached to end of expression.
        """
        if self.pos >= len(self.expr):
            raise StopIteration

        for cls_lexer in self.lexers:
            if cls_lexer.match(self.char):
                lexer: UnitLexer = cls_lexer(self.expr, self.pos)
                tok = lexer.get_token()
                self.pos += len(tok.value)
                self.advance()
                return tok

        raise self.illegal_char_error()

    __next__ = next_token

    def __iter__(self) -> Self:
        """Nothing special just returns itself."""
        return self


def lex(
    expr: str,
    ignore_chars: str = " \t\n\r",
    lexers: Iterable[type[UnitLexer]] = default_lexers,
) -> Iterator[Token]:
    """Provides an iterator to iterate through tokens.

    Arguments:
    - expr: expression.
    - ignore_chars: characters to ignore while tokenising.
    - lexers: An internal implementation to lexers to tokenise the serveral different parts of expression.
    """
    return iter(Lexer(expr=expr, ignore=ignore_chars, lexers=lexers))
