import json


__all__ = (
    'Expr',
    'BinOp',
    'Num',
    'UnaryOp',
    'FnCall',
    'Const',
    'View',
    'Node'
)

class Expr:
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self) -> str:
        return f"Expr({self.expr!r})"
    
    __str__ = __repr__


class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self) -> str:
        return f"BinOp({self.left!r}{self.op}{self.right!r})"
    
    __str__ = __repr__


class Num:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self) -> str:
        return f"Num({self.value!r})"
    
    __str__ = __repr__


class UnaryOp:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    
    def __repr__(self) -> str:
        return f"UnaryOp({self.op}{self.expr!r})"
    
    __str__ = __repr__


class FnCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args
    
    def __repr__(self) -> str:
        return "%s(%s)" % (self.name, ', '.join(map(str, self.args)))
    
    __str__ = __repr__


class Const:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self) -> str:
        return f"Const({self.name})"

    __str__ = __repr__


Node = Expr | BinOp | UnaryOp | Num | FnCall | Const


class View:
    """View object for ast."""

    def Unknown(node: object) -> dict:
        return {
            "Type": "Unknown",
            "Name": node.__class__.__name__,
            "Repr": node.__repr__(),
        }
    
    def get(node: Node) -> dict:
        """If type of node is known returns dictionary view of it.
        Otherwise returns None"""
        if isinstance(node, Expr):
            return View.Expr(node)
        elif isinstance(node, BinOp):
            return View.BinOp(node)
        elif isinstance(node, UnaryOp):
            return View.UnaryOp(node)
        elif isinstance(node, FnCall):
            return View.FnCall(node)
        elif isinstance(node, Num):
            return View.Num(node)
        elif isinstance(node, Const):
            return View.Const(node)
        else:
            return View.Unknown(node)
    
    def Expr(node: Expr) -> dict:
        return {
            "Type": "Expr",
            "Expr": View.get(node.expr)
        }
    
    def BinOp(node: BinOp) -> dict:
        return {
            "Type": "BinOp",
            "Left": View.get(node.left),
            "Op": node.op,
            "Right": View.get(node.right)
        }
    
    def UnaryOp(node: UnaryOp) -> dict:
        return {
            "Type": "UnaryOp",
            "Op": node.op,
            "Expr": View.get(node.expr)
        }
    
    def Num(node: Num) -> dict:
        return {
            "Type": "Num",
            "Value": node.value.__str__(),
        }
    
    def FnCall(node: FnCall) -> dict:
        return {
            "Type": "FnCall",
            "Name": node.name,
            "Args": list(map(View.get, node.args))
        }
    
    def Const(node: Const) -> dict:
        return {
            "Type": "Const",
            "Name": node.name
        }

    def save(node: Node, file: str):
        """Saves the node view (as dict) in given file in JSON format."""
        if not isinstance(node, dict):
            node = View.get(node)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(node, indent=4, sort_keys=False))

