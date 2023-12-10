"""
The package contains the lexers for each kind of token
"""

from .delimiter_lexer import DelimiterLexer
from .identifier_lexer import IdentifierLexer
from .number_lexer import NumberLexer
from .operator_lexer import OperatorLexer

lexers = [
    DelimiterLexer,
    IdentifierLexer,
    NumberLexer,
    OperatorLexer,
]
