"""
This package contains Parser class for parsing stream of tokens to ast.
"""

from typing import Callable, Iterator

from .node import BinOp, UnOp, Num, Func, Const
from .exceptions import InvalidTokenError, MissingSymbolError, UnexpectedEndOfInputError
from ..lexer.token import TokenType, Token

# TODO - currently some errors aren't providing much of information and there might be
# clash between InvalidTokenError and MissingSymbolError that which one should be used
# or to be renamed properly. Unexpected enf of input also needs to be improved

# TODO - tested only for few correct expressions manually

_Lexer = Callable[[str], Iterator[Token]]

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
                raise self.missing_symbol_error()

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
                raise self.missing_symbol_error()

            node = BinOp(left=node, op=op, right=self.parse_factor())

        return node

    def parse_factor(self) -> Num | UnOp | Func | Const:
        """"parses factors"""
        if self.token is None:
            raise self.unexpected_end_of_input_error()

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

        raise self.invalid_token_error()

    def missing_symbol_error(self) -> MissingSymbolError:
        return MissingSymbolError(
            self.expr,
            "You propbably need to recheck the input",
            self.token.index,
        )

    def invalid_token_error(self) -> InvalidTokenError:
        return InvalidTokenError(
            self.expr,
            self.token,
        )

    def unexpected_end_of_input_error(self) -> UnexpectedEndOfInputError:
        return UnexpectedEndOfInputError(
            self.expr,
            "expected complete expression",
        )


def parse(expr: str, lexer: _Lexer) -> Num | UnOp | Func | BinOp | Const:
    """returns ast of expr"""
    return Parser(expr, lexer).parse()
