"""
This module contains the implementation for lexing int/float in expression.
"""

from io import StringIO

from ..token import Token, TokenType
from ..atomic_lexer import AtomicLexer


class NumberLexer(AtomicLexer):

    @staticmethod
    def match(char: str) -> bool:
        return char.isdigit()

    def get_token(self) -> Token:
        stream = StringIO()
        pos = self.index
        char = self.expr[pos]

        # capturing digits before dot
        while char and char.isdigit():
            stream.write(char)
            char, pos = self.advance(pos)

        # capturing digits after dot
        if char and char == '.':
            stream.write(char)
            char, pos = self.advance(pos)

            while char and char.isdigit():
                stream.write(char)
                char, pos = self.advance(pos)

        # capturing rest part after e
        if char and char in 'eE':
            stream.write('e')
            char, pos = self.advance(pos)

            if char in '+-':
                stream.write(char)
                char, pos = self.advance(pos)

            while char and char.isdigit():
                stream.write(char)
                char, pos = self.advance(pos)

        return Token(TokenType.NUMBER, stream.getvalue(), self.index)
