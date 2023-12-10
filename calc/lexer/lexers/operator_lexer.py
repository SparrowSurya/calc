"""
This module contains the implementation for lexing operator in expression.

Operators:
```py
add = '+'
subtract = '-'
multiply = '*'
divide = '/'
mod = '%'
power = '**'
```

"""

import re

from ..token import Token, TokenType
from ..atomic_lexer import AtomicLexer


class OperatorLexer(AtomicLexer):
    max_operator_length = 2
    operators = {
        '**': TokenType.POW,
        '%': TokenType.MOD,
        '/': TokenType.DIV,
        '*': TokenType.MUL,
        '-': TokenType.MINUS,
        '+': TokenType.PLUS,
    }

    @staticmethod
    def match(char: str) -> bool:
        return char in OperatorLexer.operators.keys()

    def get_token(self) -> Token:
        start = self.index
        end = start + self.max_operator_length
        strip = self.expr[start:end]

        for symbol, token_type in self.operators.items():
            if (match := re.match(re.escape(symbol), strip)):
                end = match.end()
                value = self.expr[self.index:self.index+end]
                return Token(token_type, value, self.index)

        raise RuntimeError("Unable to extract next token")
