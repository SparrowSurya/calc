"""
Module: calc.parser
Description: Provides the classes and functions to parse the tokens.

Usage:
>>> from calc.parser import Parser, parse
>>> from calc.lexer import lex
>>> p = Parser('2+3', lex)
>>> p.parse()
BinOp(Num(2)+Num(3))
>>> parse('2+3')
BinOp(Num(2)+Num(3))
"""


from .node import BinOp, UnOp, Num, Func, Const
from .exceptions import UnknownTokenError, SyntaxError
from ..lexer import lex
from ..lexer.token import TokenType, Token
from ..types import _Lexer


__all__ = (
    "Parser",
    "parse",
)


class Parser:
    """A Parser class to convert the stream of tokens into abstract syntax tree."""

    def __init__(self, expr: str, lexer: _Lexer):
        """
        Arguments:
        - expr: expression.
        - lexer: lexer object to tokenise the expression into stream of tokens.
        """
        self.expr = expr
        self.lexer = iter(lexer(self.expr))
        self.token: Token | None = None
        self.advance()

    def advance(self):
        """Moves to next token in the expression.

        NOTE: sets token to None when tokens finished."""
        try:
            self.token = next(self.lexer)
        except StopIteration:
            self.token = None

    def parse(self) -> Num | UnOp | Func | BinOp | Const:
        """Main method to parse the expression.

        Returns:
        - A tree like node object.

        NOTE: In case of empty expression producing no tokens returns a single node with '0' value
        """
        if self.token:
            return self.parse_expr()
        return Num(0, "0")

    def parse_expr(self) -> BinOp | UnOp | Num | Func | Const:
        """Parses the expression."""
        node = self.parse_term()

        while self.token and self.token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.token.value
            index = self.token.index
            if self.token.type == TokenType.PLUS:
                self.advance()
            elif self.token.type == TokenType.MINUS:
                self.advance()
            else:
                raise self.syntax_error()

            node = BinOp(index, left=node, op=op, right=self.parse_term())

        return node

    def parse_exprs(self) -> tuple[BinOp | UnOp | Num | Func | Const]:
        """Parses expressions seperated by comma delimiter."""
        nodes = [self.parse_expr()]

        while self.token and self.token.type == TokenType.COMMA:
            self.advance()
            nodes.extend(self.parse_exprs())

        return tuple(nodes)

    def parse_term(self) -> Num | UnOp | Func | BinOp | Const:
        """Parses terms in the expression."""
        node = self.parse_factor()

        types = (TokenType.MUL, TokenType.DIV, TokenType.MOD, TokenType.POW)
        while self.token and self.token.type in types:
            op = self.token.value
            index = self.token.index
            if self.token.type == TokenType.MUL:
                self.advance()
            elif self.token.type == TokenType.DIV:
                self.advance()
            elif self.token.type == TokenType.MOD:
                self.advance()
            elif self.token.type == TokenType.POW:
                self.advance()
            else:
                raise self.syntax_error()

            node = BinOp(index, left=node, op=op, right=self.parse_factor())

        return node

    def parse_factor(self) -> Num | UnOp | Func | Const:
        """Parses factors in the term."""
        if self.token is None:
            raise self.syntax_error("unexpected end of expression")

        if self.token.type is TokenType.NUMBER:
            num = self.token.value
            index = self.token.index
            self.advance()
            return Num(index, num)

        if self.token.type == TokenType.LPAREN:
            self.advance()
            node = self.parse_expr()
            self.advance()
            return node

        if self.token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.token.value
            index = self.token.index
            self.advance()
            return UnOp(index, op, self.parse_factor())

        if self.token.type == TokenType.NAME:
            name = self.token.value
            index = self.token.index
            self.advance()

            if self.token and self.token.type == TokenType.LPAREN:
                self.advance()
                node = Func(index, name, tuple(self.parse_exprs()))
                self.advance()
                return node
            else:
                return Const(index, name)

        raise self.unknown_token_error()

    def syntax_error(self, *msg: object) -> SyntaxError:
        """produces exception object for syntax error."""
        return SyntaxError(
            self.expr,
            self.token,
            *msg,
        )

    def unknown_token_error(self) -> UnknownTokenError:
        """Producees excpetion object for unknown token."""
        return UnknownTokenError(
            self.expr,
            self.token,
            f"unknown token {self.token!r} encountered during parsing",
        )


def parse(expr: str, lexer: _Lexer = lex) -> Num | UnOp | Func | BinOp | Const:
    """Produces the abstract syntax tree of expression.

    Arguments:
    - expr: expression.
    - lexer: a lexer object providing stream of tokens."""
    return Parser(expr, lexer).parse()
