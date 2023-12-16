"""
This module contains the views for different objects.
"""

import json
from io import StringIO
from typing import Iterable

from ..types import _Token, _Node


def title_view(title: str, expr: str, end: str = '') -> str:
    """Title view format"""
    return f"{title}: '{expr}'{end}"


# tabular format
_col_fmt_tabular = (
    ('Pos',   '>',  3),
    ('Type',  '<',  8),
    ('Value', '<', 16),
    ('Index', '>',  5),
    ('Len',   '>',  3),
)


def _fmt_tabular() -> str:
    """f-string format for each row in table"""
    stream = StringIO()
    for i, (_, align, width) in enumerate(_col_fmt_tabular):
        template = " {%i:%c%i} " % (i, align, width)
        stream.write(template)
    return stream.getvalue()


def raw_token_view(tokens: Iterable[_Token]) -> str:
    """raw view of the tokens"""
    stream = StringIO()
    for tok in tokens:
        stream.write(f"{tok!r}\n")
    return stream.getvalue()


def tabular_token_view(tokens: Iterable[_Token]):
    """tabular view of tokens"""
    stream = StringIO()
    fmt = _fmt_tabular() + '\n'

    values = tuple(c[0] for c in _col_fmt_tabular)
    stream.write(fmt.format(*values))

    values = tuple('-'*c[2] for c in _col_fmt_tabular)
    stream.write(fmt.format(*values))

    for i, tok in enumerate(tokens):
        string = fmt.format(i, tok.type, tok.value, tok.index, tok.length)
        stream.write(string)

    return stream.getvalue()


def token_view(tokens: _Token, raw: bool = False, title: str = None) -> str:
    """token view of expression"""
    title = title_view('Tokens', title, '\n\n') if title else ''
    view = raw_token_view(tokens) if raw else tabular_token_view(tokens)
    return title + view


def ast_view(root: _Node, raw: bool = False, title: str = None) -> str:
    """ast view of expression"""
    title = title_view('Tree', title, '\n\n') if title else ''
    view = raw_ast_view(root) if raw else preety_ast_view(root)
    return title + view


def raw_ast_view(root: _Node) -> str:
    """raw ast view of expression"""
    return repr(root)


def preety_ast_view(root: _Node) -> str:
    """formatted ast view of expression"""
    return json.dumps(root.to_dict(), indent=4)


def error_view(title: str, *msg: str) -> str:
    """error view"""
    messags = '\n'.join(msg)
    return f"{title}: {messags}"


def eval_view(value: str | int | float, title: str = None) -> str:
    """evaluated view"""
    title = title_view('Eval', title, '\n= ') if title else ''
    return title + str(value)
