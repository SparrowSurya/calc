"""
expression error

syntaxerror

typeerror
    invalid character
    invalid token
    unknown node
    invalid binary operator
    invalid unary operator

nameerror
    wrong func name
    wrong const name


"""

from tokens import *

class CalcError:
    
    def UnknownCharacter(expr: str, index: int, description: str = ''):
        return TypeError(
            f"Unknown Character encountered in '{expr}'",
            f"                                {'^':>{index}}",
            description
        )
    
    def UnknownToken(token: Token, description: str = ''):
        return SyntaxError(
            f"Unknown Token encountered during parsing",
            f"Token: {token}",
            description
        )
    
    def UndefinedFunction(name: str):
        return TypeError(
            f"Undefined Function: {name}"
        )
    
    def UndefinedConstsnt(name: str):
        return TypeError(
            f"Undefined Constsnt: {name}"
        )
    
    def MissingToken(token_name: str, last_token_name: str):
        return SyntaxError(
            f"Missing Token[{token_name}] after Token[{last_token_name}]"
        )
