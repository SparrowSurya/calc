from __future__ import annotations

__all__ = (
    'INTEGER',
    'FLOAT',
    'PLUS',
    'MINUS',
    'MUL',
    'DIV',
    'MOD',
    'POW',
    'LPAREN',
    'RPAREN',
    'NAME',
    'COMMA',
    'EOE',
    'Token'
)


INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
MOD = 'MOD'
POW = 'POW'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
NAME = 'NAME'
COMMA = 'COMMA'
EOE = 'EOE'

# TODO: grammar as dict
# TODO: dict[func_name, [function, args]]
# TODO: constants


class Token:
    def __init__(self, type, value, start):
        self.type = type 
        self.value = value 
        self.start = start
    
    def __str__(self) -> str:
        """String representation of Instance.

        Example:
            Token(INTEGER, -3)
            Token(LAPREN, '(')
            Token(NAME, 'xyz')
        """
        return f"Token({self.type}, {self.value!r})"
    
    __repr__ = __str__
    
    def __eq__(self, other: Token):
        if isinstance(other, Token):
            return (self.type == other.type) and (self.value == other.value)
        return False
