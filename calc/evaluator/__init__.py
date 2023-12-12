"""
This package contains Evaluator class to evaluate an expression
"""

from ..lexer import lex
from ..parser import parse
from ..parser.node import Node, BinOp, UnOp, Num, Func, Const
from .functions import FUNCS
from .constants import CONSTS

from ..types import _Lexer, _Parser, _Func, _Const, _Num


class Evaluator:
    """Evaluator class to evaluate expression"""

    def __init__(self, lexer: _Lexer, parser: _Parser, funcs: _Func, consts: _Const):
        self.lexer = lexer
        self.parser = parser
        self.funcs = funcs
        self.consts = consts

    def eval(self, expr: str) -> _Num:
        """main eval function"""
        root = self.parser(expr, self.lexer)
        return self._eval_node(root)

    def _eval_node(self, root: Node) -> _Num:
        """evaluates a node in ast"""
        kind = type(root).__name__.lower()
        method = getattr(self, f"_eval_{kind}")
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
            return left / right
        if root.op == '%':
            return left % right
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
        fn = self.funcs[root.name.lower()]
        args = tuple(self._eval_node(arg) for arg in root.args)
        return fn(*args)

    def _eval_const(self, root: Const) -> _Num:
        """Evaluates constant node"""
        return self.consts[root.name.lower()]


# evaluator object with default values
_evaluator = Evaluator(lex, parse, FUNCS, CONSTS)

def evaluate(expr: str) -> _Num:
    """returns a value for given expression"""
    return _evaluator.eval(expr)
