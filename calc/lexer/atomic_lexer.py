"""
This class contains abstract class for matching
"""

import abc
from dataclasses import dataclass

from .token import Token


@dataclass(frozen=True, repr=False)
class AtomicLexer(abc.ABC):
    """Lexer for only one kind of token"""

    expr: str
    index: int

    def advance(self, pos: int) -> tuple[str, int]:
        """Moves to next position & updates char value.
        Handles `IndexError` as well."""
        try:
            return self.expr[pos+1], pos+1
        except IndexError:
            return '', pos+1

    @abc.abstractstaticmethod
    def match(char: str) -> bool:
        """A lazy way to check for the lexer to tokenise the
        string by matching the first character of string"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_token(self) -> Token:
        """Tokenises the given expression from index"""
        raise NotImplementedError
