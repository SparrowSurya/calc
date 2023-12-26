"""
This package contains Evaluator class to evaluate an expression
"""

from .functions import FUNCS
from .constants import CONSTS
from .exceptions import *

from ..lexer import lex
from ..parser import parse
from ..parser.node import Node, BinOp, UnOp, Num, Func, Const
from ..types import _Lexer, _Parser, _Func, _Const, _Num


# TODO - throw errors

class Evaluator:
    """Evaluator class to evaluate expression"""

    def __init__(self, expr: str, lexer: _Lexer = lex, parser: _Parser = parse, funcs: _Func = FUNCS, consts: _Const = CONSTS):
        self.expr = expr
        self.lexer = lexer
        self.parser = parser
        self.funcs = funcs
        self.consts = consts

    def eval(self) -> _Num:
        """main eval function"""
        root = self.parser(self.expr, self.lexer)
        return self._eval_node(root)

    def _eval_node(self, root: Node) -> _Num:
        """evaluates a node in ast"""
        try:
            name = f"_eval_{type(root).__name__.lower()}"
            method = getattr(self, name)
        except AttributeError:
            raise MethodNotFoundError(self.expr, name, root, 'method not found for node evaluation')
        return method(root)

    def _eval_binop(self, root: BinOp) -> _Num:
        """evaluates binary operator node"""
        left = self._eval_node(root.left)
        right = self._eval_node(root.right)

        if root.op == '+':
            return left + right

        if root.op == '-':
            return left - right

        if root.op == '*':
            return left * right

        if root.op == '/':
            try:
                return left / right
            except ZeroDivisionError:
                raise DivideByZeroError(self.expr, root.index, 'cannot divide by zero')

        if root.op == '%':
            try:
                return left % right
            except ZeroDivisionError:
                raise DivideByZeroError(self.expr, root.index, 'cannot modulo by zero')

        if root.op == '**':
            return left ** right

    def _eval_unop(self, root: UnOp) -> _Num:
        """Evaluates unary operator node"""
        expr = self._eval_node(root.expr)

        if root.op == '+':
            return +expr
        if root.op == '-':
            return -expr

    def _eval_num(self, root: Num) -> _Num:
        """Evaluates number node"""
        try:
            return int(root.value)
        except ValueError:
            pass

        base, expo = root.value, 0
        if 'e' in base:
            base, expo = base.split('e')

        base = float(base) if '.' in base else int(base)
        return base * (10 ** int(expo))

    def _eval_func(self, root: Func) -> _Num:
        """Evaluates function node"""
        try:
            name = root.name.lower()
            fn = self.funcs[name]
        except KeyError:
            raise UnknownFuncNameError(self.expr, name, root.index, 'function name not found')

        try:
            args = tuple(self._eval_node(arg) for arg in root.args)
            return fn(*args)
        except ValueError:
            raise MathDomainError(self.expr, name, root.index, 'value out of domain')
        except TypeError:
            raise WrongArgCountError(self.expr, name, root.index, 'wrong number of arguments provided')


    def _eval_const(self, root: Const) -> _Num:
        """Evaluates constant node"""
        try:
            name = root.name.lower()
            return self.consts[name]
        except KeyError:
            raise UnknownConstNameError(self.expr, name, root.index, 'const name not found')



def evaluate(
        expr: str,
        lexer: _Lexer = lex,
        parser: _Parser = parse,
        funcs: _Func = FUNCS,
        consts: _Const = CONSTS,
    ) -> _Num:
    """returns a value for given expression"""
    return Evaluator(expr, lexer, parser, funcs, consts).eval()
