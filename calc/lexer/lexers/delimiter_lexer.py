"""
This module contains the implementation for lexing delimiter in expression.

Delimiters:
```py
delimiters = '(', ')', ','
```

"""

from ..token import Token, TokenType
from ..atomic_lexer import AtomicLexer


class DelimiterLexer(AtomicLexer):
    delimiters = {
        '(': TokenType.LPAREN,
        ')': TokenType.RPAREN,
        ',': TokenType.COMMA,
    }

    @staticmethod
    def match(char: str) -> bool:
        return char in DelimiterLexer.delimiters.keys()

    def get_token(self) -> Token:
        char = self.expr[self.index]
        token_type = self.delimiters[char]
        return Token(token_type, char, self.index)
