"""
Module: calc.evaluator
Description: Providesthe classand functions to evaluate the parse tree.
"""

from .functions import default_funcs
from .constants import default_consts
from .exceptions import *
from ..lexer import lex
from ..parser import parse
from ..parser.node import Node, BinOp, UnOp, Num, Func, Const
from ..types import _Lexer, _Parser, _Func, _Const, _Num


class Evaluator:
    """A class to evaluate the expression."""

    def __init__(
        self,
        expr: str,
        lexer: _Lexer = lex,
        parser: _Parser = parse,
        funcs: _Func = default_funcs,
        consts: _Const = default_consts,
    ):
        """
        Arguments:
        - expr: expression.
        - lexer: function to tokenise the expression.
        - parser: parses the stream of token into parse tree.
        - funcs: functions.
        - consts: constants.
        """
        print(expr, lexer)
        self.expr = expr
        self.lexer = lexer
        self.parser = parser
        self.funcs = funcs
        self.consts = consts

    def eval(self) -> _Num:
        """Main method to evaluate the expreesion."""
        root = self.parser(self.expr, self.lexer)
        return self._eval_node(root)

    def _eval_node(self, root: Node) -> _Num:
        """Evaluates arbitrary node. Finds the appropriate method for the node."""
        try:
            name = f"_eval_{type(root).__name__.lower()}"
            method = getattr(self, name)
        except AttributeError:
            raise MethodNotFoundError(
                self.expr, name, root, "method not found for node evaluation"
            )
        return method(root)

    def _eval_binop(self, root: BinOp) -> _Num:
        """Evaluates the BinOp node."""
        left = self._eval_node(root.left)
        right = self._eval_node(root.right)

        if root.op == "+":
            return left + right

        if root.op == "-":
            return left - right

        if root.op == "*":
            return left * right

        if root.op == "/":
            try:
                return left / right
            except ZeroDivisionError:
                raise DivideByZeroError(self.expr, root.index, "cannot divide by zero")

        if root.op == "%":
            try:
                return left % right
            except ZeroDivisionError:
                raise DivideByZeroError(self.expr, root.index, "cannot modulo by zero")

        if root.op == "**":
            return left**right

    def _eval_unop(self, root: UnOp) -> _Num:
        """Evaluates UnOp node."""
        expr = self._eval_node(root.expr)

        if root.op == "+":
            return +expr
        if root.op == "-":
            return -expr

    def _eval_num(self, root: Num) -> _Num:
        """Evaluates Num node."""
        try:
            return int(root.value)
        except ValueError:
            pass

        base, expo = root.value, 0
        if "e" in base:
            base, expo = base.split("e")

        base = float(base) if "." in base else int(base)
        return base * (10 ** int(expo))

    def _eval_func(self, root: Func) -> _Num:
        """Evaluates Func node."""
        try:
            name = root.name.lower()
            fn = self.funcs[name]
        except KeyError:
            raise UnknownFuncNameError(
                self.expr, name, root.index, "function name not found"
            )

        try:
            args = tuple(self._eval_node(arg) for arg in root.args)
            return fn(*args)
        except ValueError:
            raise MathDomainError(self.expr, name, root.index, "value out of domain")
        except TypeError:
            raise WrongArgCountError(
                self.expr, name, root.index, "wrong number of arguments provided"
            )

    def _eval_const(self, root: Const) -> _Num:
        """Evaluates Const node."""
        try:
            name = root.name.lower()
            return self.consts[name]
        except KeyError:
            raise UnknownConstNameError(
                self.expr, name, root.index, "const name not found"
            )


def evaluate(expr: str) -> _Num:
    """
    Evaluates the expreesion into and outputs the result.

    Arguments:
    - expr: expression.
    """
    return Evaluator(expr).eval()
