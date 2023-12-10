"""
This module contains various nodes for ast
"""

from __future__ import annotations
import abc


class Node(abc.ABC):
    """Abstract base class for node in ast"""

    def from_dict(cls, obj: dict[str, Node]) -> Node:
        return cls(**obj)

    @abc.abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


class BinOp(Node):
    """Node for a binary operator"""

    def __init__(self, left: Node, op: str, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"BinOp({self.left}{self.op}{self.right})"

    def to_dict(self) -> dict:
        return {
            'left': self.left.to_dict(),
            'op': self.op,
            'right': self.right.to_dict(),
        }


class Num(Node):
    """Node for a literal number (can be int or float or
    in scientific notation)"""

    def __init__(self, value: int | float):
        self.value = value

    def __repr__(self) -> str:
        return f"Num({self.value})"

    def to_dict(self) -> dict:
        return {'value': self.value}


class UnOp(Node):
    """Node for unary operator"""

    def __init__(self, op: str, expr: Node):
        self.op = op
        self.expr = expr

    def __repr__(self) -> str:
        return f"UnaryOp({self.op}({self.expr}))"

    def to_dict(self) -> dict:
        return {
            'op': self.op,
            'expr': self.expr.to_dict(),
        }


class Func(Node):
    """Node for function object which takes in some input
    and returns a value"""

    def __init__(self, name: str, args: tuple[Node]):
        self.name = name
        self.args = args

    def __repr__(self) -> str:
        args = ', '.join(map(str, self.args))
        return f"{self.name}({args})"

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'args': [node.to_dict() for node in self.args],
        }


class Const(Node):
    """Node for a constant value represented by a name"""

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"Const({self.name.upper()})"

    def to_dict(self) -> dict:
        return {'name': self.name}
