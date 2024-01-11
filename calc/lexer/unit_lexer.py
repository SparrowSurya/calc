"""
Module: calc.lexer.unit_lexer
Description: Provides the classes to tokenise single token unit in expression.
"""

import abc
import re
from dataclasses import dataclass
from io import StringIO

from .token import TokenType, Token


__all__ = (
    "UnitLexer",
    "DelimiterLexer",
    "IdentifierLexer",
    "NumberLexer",
    "OperatorLexer",
    "default",
)


@dataclass(frozen=True, repr=False)
class UnitLexer(abc.ABC):
    """An abstract base class for unit lexer.

    The class describes the lexer which can tokenise the part of expression.
    The class may produce token of various types.

    A staticmethod is provided by the class to check if the lexer can tokenise
    the expression based on the first character of the part of expression to be tokenised.
    """

    expr: str
    """Complete expression"""

    index: int
    """Index of the expression from where the tokenisation should start."""

    def advance(self, pos: int) -> tuple[str, int]:
        """Moves the position to next character.
        Arguments:
            - pos: current index

        Return:
            1. next character ('' when reached end of string)
            2. Index of the character
        """
        try:
            return self.expr[pos + 1], pos + 1
        except IndexError:
            return "", pos + 1

    @abc.abstractstaticmethod
    def match(char: str) -> bool:
        """Lazy way to check if the lexer can tokenise the part of expression starting from
        given character.

        Arguments:
            - char: first character of the part of expression

        NOTE: Does not gurantee that on match a token will be produced.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_token(self) -> Token:
        """Tokenises the given expression from index.

        NOTE:
            1. Might fail to tokenise.
            2. Should not raise any exception explicitly, as other lexer might work.
        """
        raise NotImplementedError


class DelimiterLexer(UnitLexer):
    """Tokenises the delimiters in the expression."""

    delimiters = {
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        ",": TokenType.COMMA,
    }
    """Dictionary of delimiters mapped to the TokenType"""

    @staticmethod
    def match(char: str) -> bool:
        return char in DelimiterLexer.delimiters.keys()

    def get_token(self) -> Token:
        char = self.expr[self.index]
        token_type = self.delimiters[char]
        return Token(token_type, char, self.index)


class IdentifierLexer(UnitLexer):
    """Tokenises the identifiers in the expression."""

    @staticmethod
    def match(char: str) -> bool:
        return char.isalpha()

    def get_token(self) -> Token:
        stream = StringIO()
        pos = self.index
        char = self.expr[pos]

        while char.isalnum():
            stream.write(char)
            char, pos = self.advance(pos)

        return Token(TokenType.NAME, stream.getvalue(), self.index)


class NumberLexer(UnitLexer):
    """Tokenises the numbers in the expression"""

    @staticmethod
    def match(char: str) -> bool:
        return char.isdigit()

    def get_token(self) -> Token:
        stream = StringIO()
        pos = self.index
        char = self.expr[pos]

        # capturing digits before dot
        while char and char.isdigit():
            stream.write(char)
            char, pos = self.advance(pos)

        # capturing digits after dot
        if char and char == ".":
            stream.write(char)
            char, pos = self.advance(pos)

            while char and char.isdigit():
                stream.write(char)
                char, pos = self.advance(pos)

        # capturing rest part after e
        if char and char in "eE":
            stream.write("e")
            char, pos = self.advance(pos)

            if char in "+-":
                stream.write(char)
                char, pos = self.advance(pos)

            while char and char.isdigit():
                stream.write(char)
                char, pos = self.advance(pos)

        return Token(TokenType.NUMBER, stream.getvalue(), self.index)


class OperatorLexer(UnitLexer):
    """Tokenises the operators in the expression."""

    max_operator_length = 2
    """Maximum length of the operator in expression."""

    operators = {
        "**": TokenType.POW,
        "%": TokenType.MOD,
        "/": TokenType.DIV,
        "*": TokenType.MUL,
        "-": TokenType.MINUS,
        "+": TokenType.PLUS,
    }
    """Dictionary of operators mapped to TokenType."""

    @staticmethod
    def match(char: str) -> bool:
        return char in OperatorLexer.operators.keys()

    def get_token(self) -> Token:
        start = self.index
        end = start + self.max_operator_length
        substr = self.expr[start:end]

        for symbol, token_type in self.operators.items():
            if match := re.match(re.escape(symbol), substr):
                end = match.end()
                value = self.expr[self.index : self.index + end]
                return Token(token_type, value, self.index)

        raise RuntimeError("Unable to extract next token")


# default lexers
default = (
    DelimiterLexer,
    IdentifierLexer,
    NumberLexer,
    OperatorLexer,
)
