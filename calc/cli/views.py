"""
This module contains the views for different objects.
"""

import json
from io import StringIO
from typing import Iterable

from ..types import _Token, _Node


def expr_view(expr: str) -> str:
    return f"Expr: {expr}"


def token_view(tokens: Iterable[_Token]) -> str:
    stream = StringIO()
    fmt = " {0:>3}  {1:<8}  {2:<16}  {3:>5}  {4:>3} \n"
    columns = ('Pos', 'Type', 'Value', 'Index', 'Len')

    stream.write(fmt.format(*columns))
    for i, tok in enumerate(tokens):
        stream.write(fmt.format(i, tok.type, tok.value, tok.index, tok.length))
    return stream.getvalue()


def ast_view(node: _Node) -> str:
    dict_view = node.to_dict()
    return json.dumps(dict_view, indent=4)


def eval_view(expr: str, result: int | float | str) -> str:
    return f"{expr} = {result}"
