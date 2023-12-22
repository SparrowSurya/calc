"""
This package contains Parser class for parsing stream of tokens to ast.
"""


from .node import BinOp, UnOp, Num, Func, Const
from .exceptions import UnknownTokenError, SyntaxError
from ..lexer import lex
from ..lexer.token import TokenType, Token
from ..types import _Lexer



class Parser:
    """Parser object to convert stream of tokens to ast"""

    def __init__(self, expr: str, lexer: _Lexer):
        self.expr = expr
        self.lexer = iter(lexer(self.expr))
        self.token: Token | None = None
        self.advance()

    def advance(self):
        """move to next token"""
        try:
            self.token = next(self.lexer)
        except StopIteration:
            self.token = None

    def parse(self) -> Num | UnOp | Func | BinOp | Const:
        """main parse function"""
        if self.token:
            return self.parse_expr()
        return Num('0')

    def parse_expr(self) -> BinOp | UnOp | Num | Func | Const:
        """parses an expression"""
        node = self.parse_term()

        while self.token and self.token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.token.value
            if self.token.type == TokenType.PLUS:
                self.advance()
            elif self.token.type == TokenType.MINUS:
                self.advance()
            else:
                raise self.syntax_error()

            node = BinOp(left=node, op=op, right= self.parse_term())

        return node

    def parse_exprs(self) -> tuple[BinOp | UnOp | Num | Func | Const]:
        """parses expressions seperated by comma delimiter"""
        nodes = [self.parse_expr()]

        while self.token and self.token.type == TokenType.COMMA:
            self.advance()
            nodes.extend(self.parse_exprs())

        return tuple(nodes)

    def parse_term(self) -> Num | UnOp | Func | BinOp | Const:
        """parses terms"""
        node = self.parse_factor()

        types = (TokenType.MUL, TokenType.DIV, TokenType.MOD, TokenType.POW)
        while self.token and self.token.type in types:
            op = self.token.value
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

            node = BinOp(left=node, op=op, right=self.parse_factor())

        return node

    def parse_factor(self) -> Num | UnOp | Func | Const:
        """"parses factors"""
        if self.token is None:
            raise self.syntax_error("unexpected end of expression")

        if self.token.type is TokenType.NUMBER:
            num = self.token.value
            self.advance()
            return Num(num)

        if self.token.type == TokenType.LPAREN:
            self.advance()
            node = self.parse_expr()
            self.advance()
            return node

        if self.token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.token.value
            self.advance()
            return UnOp(op, self.parse_factor())

        if self.token.type == TokenType.NAME:
            name = self.token.value
            self.advance()

            if self.token and self.token.type == TokenType.LPAREN:
                self.advance()
                node = Func(name, tuple(self.parse_exprs()))
                self.advance()
                return node
            else:
                return Const(name)

        raise self.unknown_token_error()

    def syntax_error(self, *msg: object) -> SyntaxError:
        """returns syntax error object"""
        return SyntaxError(
            self.expr,
            self.token,
            *msg,
        )

    def unknown_token_error(self) -> UnknownTokenError:
        """returns unknown token error object"""
        return UnknownTokenError(
            self.expr,
            self.token,
            f"unknown token {self.token!r} encountered during parsing"
        )


def parse(expr: str, lexer: _Lexer = lex) -> Num | UnOp | Func | BinOp | Const:
    """returns ast of expr"""
    return Parser(expr, lexer).parse()
