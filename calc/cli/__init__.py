"""
This package contains objects and functions required for parsing and
output command line arguments for calc.
"""

from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Iterable

from ..lexer import lex
from ..parser import parse
from ..evaluator import evaluate
from ..exceptions import CalcError
from .views import token_view, ast_view, eval_view, error_view



@dataclass(frozen=True)
class Args:
    """Parse command line arguments provided to calc module"""

    exprs: Iterable[str]
    raw: bool = False
    title: bool = True
    fmt: str = None
    show_eval: bool = True
    color: bool = True
    inspect_tokens: bool = False
    inspect_tree: bool = False
    round: int | None = None


def get_argparser() -> ArgumentParser:
    """returns th aprser object to parse args"""
    p = ArgumentParser('calc')

    p.add_argument('--no-eval', action='store_const', const=False, default=True, required=False, help="do not output the value evaluated")
    p.add_argument('--no-title', action='store_const', const=False, default=True, required=False, help="do not show title for given output")
    p.add_argument('--raw', action='store_const', const=True, default=False, help="show output without formatting")
    p.add_argument('--no-color', action='store_const', const=False, default=True, help="do not colorise output")

    p.add_argument('--inspect-tokens', action='store_const', const=True, default=False, required=False, help="inspect tokens of the expression")
    p.add_argument('--inspect-tree', action='store_const', const=True, default=False, required=False, help="inspect parse tree of the expression")

    p.add_argument('-r', '--round', type=int, default=None, required=False, help="round output value")
    p.add_argument('-f', '--format', type=str, default=None, required=False, help="python f-string based format specifier to format number")

    p.add_argument('-e', '--expr', '--exprs', required=True, nargs='+', help="input expressions")

    return p


def parse_args(arg_parser: ArgumentParser, argv: Iterable[str]) -> Args:
    """returns parsed data"""
    args = arg_parser.parse_args(argv)
    return Args(
        exprs=args.expr,
        raw=args.raw,
        title=args.no_title,
        fmt=args.format,
        show_eval=args.no_eval,
        color=args.no_color,
        inspect_tokens=args.inspect_tokens,
        inspect_tree=args.inspect_tree,
        round=args.round,
    )


def process(expr: str, args: Args):
    """Processes one expression at a time"""

    try:
        tokens = tuple(tok for tok in lex(expr))
        root = parse(expr, lex)
        result = evaluate(expr)

        if args.round:
            result = round(result, args.round)

        if args.fmt:
            result = format(result, args.fmt)

    except CalcError as e:
        name, desc = str(e).split(': ', maxsplit=1)
        print(error_view(name, desc, color=args.color))
        return

    title = expr if args.title else None

    if args.inspect_tokens:
        print(token_view(tokens, args.raw, title, args.color), end='\n\n')

    if args.inspect_tree:
        print(ast_view(root, args.raw, title, args.color), end='\n\n')

    if args.show_eval:
        print(eval_view(result, title, args.color), end='\n\n')


def main(argv):
    """Main functions for CLI"""
    args = parse_args(arg_parser=get_argparser(), argv=argv)
    for expr in args.exprs:
        process(expr, args)
