"""
This module contains the implementation for lexing identifier in expression.
"""

from io import StringIO

from ..token import Token, TokenType
from ..atomic_lexer import AtomicLexer


class IdentifierLexer(AtomicLexer):

    @staticmethod
    def match(char: str) -> bool:
        return char.isalpha()

    def get_token(self) -> Token:
        stream = StringIO()
        pos = self.index
        char = self.expr[pos]

        while char.isalnum():
            stream.write(char)
            char, pos = self.advance(pos)

        return Token(TokenType.NAME, stream.getvalue(), self.index)
