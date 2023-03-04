from typing import Callable
import math

from evaluator.ast_ import *

class Fn:
    def __init__(self, name: str, callback: Callable, argc: int, req: int):
        self.name = name
        self.call = callback
        self.argc = argc 
        self.areq = req 
    
    def __str__(self) -> str:
        return self.name
    
    def __call__(self, *args) -> int | float:
        return self.call(*args)


func: dict[str, tuple[Callable, int]] = {
    'sin'  : (math.sin, 1),
    'cos'  : (math.cos, 1),
    'asin' : (math.asin, 1),
    'acos' : (math.acos, 1),
    'atan' : (math.atan, 1),
    'sinh' : (math.sinh, 1),
    'cosh' : (math.cosh, 1),
    'tanh' : (math.tanh, 1),
    'asinh': (math.asinh, 1),
    'acosh': (math.acosh, 1),
    'atanh': (math.atanh, 1),
    'log10': (math.log10, 1),
    'log2' : (math.log2, 1),
    'log'  : (math.log, 2),
    'floor': (math.floor, 1),
    'ceil' : (math.ceil, 1),
    'sqrt' : (math.sqrt, 1),
    'cbrt' : (math.cbrt, 1),
    'abs'  : (abs, 1),
    'max'  : (max, 0),
    'min'  : (min, 0),
    'round': (round, 2),
    'avg'  : (lambda *x: sum(x)/len(x), 0)
}

const: dict[str, int | float] = {
    'pi': math.pi,
    'e' : math.e
}

class Interpreter:

    def __init__(self, functions: dict[str, tuple[Callable, int]], constants: dict[str, int | float]):
        self.funcs = functions
        self.consts = constants
    
    def add_func(self, name: str, fn: Callable, argc: int):
        if name in self.funcs.keys():
            raise TypeError(f"function[{name}] already defined")
        self.funcs[name] = (fn, argc)
    
    def add_const(self, name: str, value: int | float):
        if name in self.consts.keys():
            raise TypeError(f"constant[{name}] already defined")
        self.consts[name] = value

    def eval(self, node: Node) -> int | float:
        if isinstance(node, Num):
            return self.visit_num(node)
        elif isinstance(node, BinOp):
            return self.visit_binop(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unaryop(node)
        elif isinstance(node, FnCall):
            return self.visit_func(node)
        elif isinstance(node, Expr):
            return self.visit_expr(node)
        elif isinstance(node, Const):
            return self.visit_const(node)
        else:
            self.visit_unknown(node)
    
    def visit_unknown(self, node):
        raise ValueError(f"Cannot visit node[{node!r}]")
    
    def visit_expr(self, node: Expr) -> int | float:
        return self.eval(node.expr)

    def visit_num(self, node: Num) -> int | float:
        return node.value
    
    def visit_func(self, node: FnCall) -> int | float:
        fn, argc = self.funcs[node.name]

        if node.name not in self.funcs.keys():
            raise NameError(f"function[{node.name}] is not defined")
        
        if argc!=0 and argc!=len(node.args):
            raise TypeError(f"{node.name} requires {argc} arguments but got {len(node.args)} arguments")
        
        args = tuple(map(self.eval, node.args))
        return fn(*args)
    
    def visit_binop(self, node: BinOp) -> int | float:
        left = self.eval(node.left)
        right = self.eval(node.right)
        op = node.op

        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '%':
            return left % right
        elif op == '^':
            return left ** right
        else:
            raise TypeError(f"Binary Operator[{op}] is not defined")
    

    def visit_unaryop(self, node: UnaryOp) -> int | float:
        value = self.eval(node.expr)
        op = node.op
        if  op == '+':
            return value
        elif op == '-':
            return -value
        else:
            raise TypeError(f"Unary Operator[{op}] is not defined")

    def visit_const(self, node: Const) -> int | float:
        if node.name not in self.consts.keys():
            raise NameError(f"Constant[{node.name}] is not defined")
        return self.consts[node.name]
