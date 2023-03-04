import json

from evaluator.lexer import * 
from evaluator.parser_ import *
from evaluator.ast_ import *


def dump_ast_view(expr: str, file: str = 'dump.json'):
    """Dumps the given `expr` into given file in json format"""
    View.save(View.get(Parser([token for token in Lexer(expr)]).parse()), file)


def dump_ast(node: Expr, file: str = 'debug_ast.json') -> None:
    """Dumps the parsed `node` into given file in json format using `View` object"""
    data_dict = View.get(node)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_dict, sort_keys=False, indent=4))


def dump_tokens(tokens: list, file: str = 'debug_ast.json') -> None:
    """Dumps the `tokens` into given file in json format"""
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(tokens, sort_keys=False, indent=4))

