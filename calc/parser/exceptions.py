"""
This module contains exception classes raised during parsing
"""

from ..lexer.token import Token


class InvalidTokenError(Exception):
    """Raised when there is a new token in lexer but parser dont supports it yet"""

    def __init__(self, expr: str, token: Token):
        self.expr = expr
        self.token = token

    def __str__(self) -> str:
        marker = '^'*self.token.length
        return '\n'.join([
            f"Invalid Token: <{self.token}> encountered during parsing",
            self.expr,
            f"{marker:>{self.token.index}}"
        ])


class MissingSymbolError(Exception):
    """Raised when a symbol (probably an operator) is missing"""

    def __init__(self, expr: str, symbol: str, pos: int):
        self.expr = expr
        self.symbol = symbol
        self.pow = pos

    def __str__(self) -> str:
        return '\n'.join([
            f"Missing Symbol: {self.symbol} expected at {self.pos}",
            self.expr,
            f"{'^':>{self.pos}}",
        ])


class UnexpectedEndOfInputError(Exception):
    """Raised when given incomplete expression"""

    def __init__(self, expr: str, expected: str):
        self.expr = expr
        self.expected = expected

    def __str__(self) -> str:
        return 'n'.join([
            f"Unexpected End of Input: {self.expected}",
            f"Expr: {self.expr}",
        ])

