"""
This module contains the views for different objects.
"""

import json
from io import StringIO
from typing import Iterable

from .styles import *
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


def raw_token_view(tokens: Iterable[_Token], color: bool = False) -> str:
    """raw view of the tokens"""
    return '\n'.join(map(repr, tokens))


def tabular_token_view(tokens: Iterable[_Token], color: bool = False, fmt: str = _fmt_tabular()):
    """tabular view of tokens"""
    rows = []

    headings = tuple(c[0] for c in _col_fmt_tabular)
    seperators = tuple('-'*c[2] for c in _col_fmt_tabular)

    if color:
        rows.append(wrap(fmt.format(*headings), LT_GREEN_FG, LT_WHITE_FG))
        rows.append(wrap(fmt.format(*seperators), LT_GREEN_FG, LT_WHITE_FG))
    else:
        rows.append(fmt.format(*headings))
        rows.append(fmt.format(*seperators))

    for i, tok in enumerate(tokens):
        string = fmt.format(i, tok.type, tok.value, tok.index, tok.length)
        rows.append(string)

    return '\n'.join(rows)


def token_view(tokens: _Token, raw: bool = False, title: str = None, color: bool = False) -> str:
    """token view of expression"""
    title = title_view('Tokens', title, '\n\n') if title else ''
    view = raw_token_view(tokens, color) if raw else tabular_token_view(tokens, color)
    return title + view


def ast_view(root: _Node, raw: bool = False, title: str = None, color: bool = False) -> str:
    """ast view of expression"""
    title = title_view('Tree', title, '\n\n') if title else ''
    view = raw_ast_view(root, color) if raw else preety_ast_view(root, color)
    return title + view


def raw_ast_view(root: _Node, color: bool = False) -> str:
    """raw ast view of expression"""
    return repr(root)


def preety_ast_view(root: _Node, color: bool = False) -> str:
    """formatted ast view of expression"""
    return json.dumps(root.to_dict(), indent=4)


def error_view(title: str, *msg: str, color: bool = False) -> str:
    """error view"""
    if color:
        title = wrap(title, LT_RED_FG, LT_WHITE_FG)
    messags = '\n'.join(msg)
    return f"{title}: {messags}"


def eval_view(value: str | int | float, title: str = None, color: bool = False) -> str:
    """evaluated view"""
    title = title_view('Eval', title, '\n= ') if title else ''
    value = str(value)
    return title + wrap(value, LT_GREEN_FG, DK_WHITE_FG) if color else title + value
