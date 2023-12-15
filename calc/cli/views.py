"""
This module contains the views for different objects.
"""

import json
from io import StringIO
from typing import Iterable

from ..view import View
from ..types import _Token, _Node


class TerminalView(View):
    """Viewer object for expression in terminal"""

    _col_fmt_tabular = (
        ('Pos',   '>',  3),
        ('Type',  '<',  8),
        ('Value', '<', 16),
        ('Index', '>',  5),
        ('Len',   '>',  3),
    )

    def _fmt_tabular(self) -> str:
        """f-string format for each row in table"""
        stream = StringIO()
        for i, (_, align, width) in enumerate(self._col_fmt_tabular):
            template = " {%i:%c%i} " % (i, align, width)
            stream.write(template)
        return stream.getvalue()

    def raw_token_view(self, tokens: Iterable[_Token]) -> str:
        """raw view of the tokens"""
        stream = StringIO()
        for tok in tokens:
            stream.write(f"{tok!r}\n")
        return stream.getvalue()

    def tabular_token_view(self, tokens: Iterable[_Token]):
        """tabular view of tokens"""
        stream = StringIO()
        fmt = self._fmt_tabular() + '\n'

        values = tuple(c[0] for c in self._col_fmt_tabular)
        stream.write(fmt.format(*values))

        values = tuple('-'*c[2] for c in self._col_fmt_tabular)
        stream.write(fmt.format(*values))

        for i, tok in enumerate(tokens):
            string = fmt.format(i, tok.type, tok.value, tok.index, tok.length)
            stream.write(string)

        return stream.getvalue()

    def token_view(self, tokens: _Token, raw: bool = False):
        """token view of expression"""
        return self.raw_token_view(tokens) if raw else self.tabular_token_view(tokens)

    def ast_view(self, root: _Node, raw: bool = False) -> str:
        """ast view of expression"""
        return self.raw_ast_view(root) if raw else self.preety_ast_view(root)

    def raw_ast_view(self, root: _Node) -> str:
        """raw ast view of expression"""
        return repr(root)

    def preety_ast_view(self, root: _Node) -> str:
        """formatted ast view of expression"""
        return json.dumps(root.to_dict(), indent=4)

    def expr_view(self, expr: str) -> str:
        """expression view"""
        return f"Expr: '{expr}'"

    def eval_view(self, expr: str, result: str) -> str:
        """expression evaluation view"""
        return f"{expr} = {result}"

    def error_view(self, title: str, *msg: str) -> str:
        """error view"""
        messags = '\n'.join(msg)
        return f"{title}: {messags}"
