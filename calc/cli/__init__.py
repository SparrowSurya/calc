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
from .views import TerminalView



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
    raw: bool
    output: Output = Output.EVAL
    round: int | None = None


def get_argparser() -> ArgumentParser:
    """returns th aprser object to parse args"""
    p = ArgumentParser('Calc')

    p.add_argument('-o', '--output', choices=Output.choices(), default='EVAL', required=False, help="ouptut view")
    p.add_argument('-r', '--round', type=int, default=None, required=False, help="round output value")
    p.add_argument('--raw', action="store_const", const=True, default=False, help="View output without formatting")
    p.add_argument('-e', '--expr', '--exprs', required=True, nargs='+', help="expressions")

    return p


def parse_args(arg_parser: ArgumentParser, argv: Iterable[str]) -> Args:
    """retursn parsed args in a data structure"""
    args = arg_parser.parse_args(argv)
    return Args(
        exprs=args.expr,
        raw=args.raw,
        output=Output.from_names(args.output),
        round=args.round,
    )


# TODO - error handelling
def process(expr: str, args: Args):
    """Processes one expression at a time"""
    if (output := args.output) == Output.NONE:
        return

    tokens = tuple(tok for tok in lex(expr))
    root = parse(expr, lex)
    result = evaluate(expr)
    viewer = TerminalView()

    print('', viewer.expr_view(expr), sep='\n', end='\n\n')

    if output & Output.TOKEN or output == Output.ALL:
        print("Tokens:", viewer.token_view(tokens, args.raw), sep='\n')

    if output & Output.AST or output == Output.ALL:
        print("AST:", viewer.ast_view(root, args.raw), end='\n\n')

    if output & Output.EVAL or output == Output.ALL:
        if args.round:
            result = round(result, args.round)
        print("Eval:", viewer.eval_view(expr, result))


def main(argv):
    """Main functions for CLI"""
    args = parse_args(arg_parser=get_argparser(), argv=argv)
    for expr in args.exprs:
        process(expr, args)
