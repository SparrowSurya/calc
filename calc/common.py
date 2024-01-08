"""
This module contains common interface for key data
exchange between view and model.
"""

from dataclasses import dataclass
from enum import Enum, auto


class KeyKind(Enum):
    """
    Describes the kind of operation to be performed
    """

    EQUAL = auto()
    BACKSPACE = auto()
    CLEAR = auto()
    INSERT = auto()  # requires the associated data


@dataclass
class KeyData:
    """
    Dataclass to store the action with associated data
    """

    kind: KeyKind
    char: str = ""


class Response(Enum):
    """
    Describes the kind of response from model.
    """

    EVAL = auto()
    ERROR = auto()
    EXPR = auto()


@dataclass
class Result:
    """
    Dataclass to store the response from model
    """

    response: Response
    expr: str
    data: object = None  # exception or evaluated result
