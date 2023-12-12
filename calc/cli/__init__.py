"""
This package contains objects and functions required for parsing and
output command line arguments for calc.
"""

from argparse import ArgumentParser
from dataclasses import dataclass
from enum import IntFlag, auto
from typing import Iterable

from ..lexer import lex
from ..parser import parse
from ..evaluator import evaluate
from .views import expr_view, token_view, ast_view, eval_view


class Output(IntFlag):
    """Output view of the input.

    Views:
        * none: no views
        * token: view tokens
        * ast: view parsed tree
        * eval: view the final evaluated result
        * all: view all of above
    """

    NONE  = 0
    TOKEN = auto()
    AST   = auto()
    EVAL  = auto()
    ALL   = TOKEN | AST | EVAL

    @classmethod
    def from_names(cls, *flag_names: str):
        """returns View object based on the flag names"""
        flag_value = 0
        for flag_name in flag_names:
            try:
                flag_value |= cls[flag_name.upper()]
            except KeyError:
                raise ValueError(f"Invalid view flag name: {flag_name}, choices: {cls.choices()}")
        return cls(flag_value)

    @staticmethod
    def choices() -> tuple[str]:
        return tuple(Output.__members__.keys())


@dataclass(frozen=True)
class Args:
    """Parse command line arguments provided to calc module"""

    exprs: Iterable[str]
    output: Output = Output.EVAL
    round: int | None = None


def get_argparser() -> ArgumentParser:
    """returns th aprser object to parse args"""
    p = ArgumentParser('Calc')

    p.add_argument('-o', '--output', choices=Output.choices(), default='EVAL', required=False)
    p.add_argument('-r', '--round', type=int, default=None, required=False)
    p.add_argument('-e', '--expr', '--exprs', required=True, nargs='+')

    return p


def parse_args(arg_parser: ArgumentParser, argv: Iterable[str]) -> Args:
    """retursn parsed args in a data structure"""
    args = arg_parser.parse_args(argv)
    return Args(
        exprs=args.expr,
        output=Output.from_names(args.output),
        round=args.round,
    )


def process(expr: str, args: Args):
    """Processes one expression at a time"""
    output = args.output

    if output == output.NONE:
        return

    print('', expr_view(expr), sep='\n', end='\n\n')

    if output & Output.TOKEN or output == Output.ALL:
        print("Tokens:")
        print(token_view(lex(expr)))

    if output & Output.AST or output == Output.ALL:
        print("AST:")
        print(ast_view(parse(expr, lex)), end='\n\n')

    if output & Output.EVAL or output == Output.ALL:
        value = evaluate(expr)
        if args.round:
            value = round(value, args.round)
        print("Evaluated:")
        print(eval_view(expr, value))


def main(argv):
    """Main functions for CLI"""
    args = parse_args(arg_parser=get_argparser(), argv=argv)
    for expr in args.exprs:
        process(expr, args)
