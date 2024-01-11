"""
Module: calc.parser.node
Description: It contains the node classes for parse tree.
"""

from __future__ import annotations
import abc


__all__ = (
    "Node",
    "BinOp",
    "UnOp",
    "Num",
    "Func",
    "Const",
)


class Node(abc.ABC):
    """An abstract base class for node in parse tree."""

    def __init__(self, index: int):
        """
        Arguments:
        - index: representing the node position in expression.
        """
        self.index = index

    @classmethod
    def from_dict(cls, data: dict[str, Node]) -> Node:
        """A utility class method to construct the node object from data.

        Arguments:
        - data: data required to build the class object.

        NOTE: keys of the data must match the respective parameter names of the class.
        """
        return cls(**obj)

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """A utility method to get the node data."""
        raise NotImplementedError


class BinOp(Node):
    """Node for a binary operator.

    A binary operator takes two operands and produces a single value."""

    def __init__(self, index: str, left: Node, op: str, right: Node):
        """
        Arguments:
        - index: position of node in expression.
        - left: left operand.
        - op: binary operator.
        - right: right operand
        """
        super().__init__(index)
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"BinOp({self.left}{self.op}{self.right})"

    def to_dict(self) -> dict:
        return {
            "left": self.left.to_dict(),
            "op": self.op,
            "right": self.right.to_dict(),
        }


class Num(Node):
    """Node for a number.

    The number can be int or float or in a scientific form."""

    def __init__(self, index: str, value: str):
        """
        Arguments:
        - index: position of node in expression.
        - value: number.
        """
        super().__init__(index)
        self.value = value

    def __repr__(self) -> str:
        return f"Num({self.value})"

    def to_dict(self) -> dict:
        return {"value": self.value}


class UnOp(Node):
    """Node for unary operator.

    A unary operator takes one operand an produces a single value."""

    def __init__(self, index: str, op: str, expr: Node):
        """
        Arguments:
        - index: position of node in expression.
        - op: unary operator.
        - expr: operand of the operator.
        """
        super().__init__(index)
        self.op = op
        self.expr = expr

    def __repr__(self) -> str:
        return f"UnaryOp({self.op}({self.expr}))"

    def to_dict(self) -> dict:
        return {
            "op": self.op,
            "expr": self.expr.to_dict(),
        }


class Func(Node):
    """Node for a function.

    A function takes atleast one argument and produces a single value."""

    def __init__(self, index: str, name: str, args: tuple[Node]):
        """
        Arguments:
        - index: position of node in expression.
        - name: name of the function.
        - args: arguments passed to the function.
        """
        super().__init__(index)
        self.name = name
        self.args = args

    def __repr__(self) -> str:
        args = ", ".join(map(str, self.args))
        return f"{self.name}({args})"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "args": [node.to_dict() for node in self.args],
        }


class Const(Node):
    """Node for a constant.

    A constant is a numerical value which has a fixed value."""

    def __init__(self, index: str, name: str):
        """
        Arguments:
        - index: position of node in expression.
        - name: name of the constant.
        """
        super().__init__(index)
        self.name = name

    def __repr__(self) -> str:
        return f"Const({self.name.upper()})"

    def to_dict(self) -> dict:
        return {"name": self.name}
