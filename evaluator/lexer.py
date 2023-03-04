from typing import Self 

from evaluator.tokens import * 


__all__ = ('Lexer',)

class Lexer:
    def __init__(self, expr):
        self.expr = expr
        self._gen = iter(self.expr)
        self.pos = 0
        self.current_char = next(self._gen)
    
    def __iter__(self) -> Self:
        return self
    
    def __call__(self, new_expr: str) -> Self:
        self.expr = new_expr
        self._gen = iter(self.expr)
        self.pos = 0
        self.current_char = next(self._gen)
        return
    
    def tokenise(self) -> list[Token]:
        return [token for token in self]
    
    def advance(self) -> None:
        """Advance the `pos` index-pointer and set the `current_char` variable."""
        try:
            self.current_char = next(self._gen)
            self.pos += 1
        except StopIteration:
            self.expr = None
            self._gen = None
            self.pos = 0
            self.current_char = None
    
    def error(self):
        return TypeError(f"Invalid character '{self.current_char}' at {self.pos} in {self.expr}")
    
    def peek(self) -> str:
        peek_pos += 1
        if self.pos > len(self.expr)-1:
            return None
        return self.expr[peek_pos]
    
    def skip_whitespace(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def name(self) -> Token:
        """"Returns name from the `pos` index-pointer."""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return Token(NAME, result, self.pos-len(result))
    
    def number(self) -> Token:
        """Returns a integer or float token from the `pos` index-pointer."""
        base = ''
        is_float = False
        expo = ''
        
        # capturing digits before dot
        while self.current_char is not None and self.current_char.isdigit():
            base += self.current_char
            self.advance()

        # capturing digits after dot
        if self.current_char == '.':
            is_float = True
            base += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                base += self.current_char
                self.advance()

        # capturing rest part from e
        if self.current_char == 'e' or self.current_char == 'E':
            self.advance()

            if self.current_char == '+' or self.current_char == '-':
                expo += self.current_char
                self.advance()
            
            while self.current_char is not None and self.current_char.isdigit():
                expo += self.current_char
                self.advance()
        
        pos = self.pos - len(base) - len(expo) - 1
        expo = int(expo) if expo else 0
        
        if is_float:
            num = float(base) * (10**expo)
            return Token(FLOAT, num, pos) 
        else:
            num = int(base) * (10**expo)
            if isinstance(num, int):
                return Token(INTEGER, num, pos)
            else:
                return Token(FLOAT, num, pos)


    def __next__(self) -> Token:
        """Lexical analyzer
        
        This breaks an expression apart into a token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self.name()

            if self.current_char.isdigit():
                return self.number()
            
            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',', self.pos-1)

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+', self.pos-1)

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-', self.pos-1)

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*', self.pos-1)

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/', self.pos-1)

            if self.current_char == '%':
                self.advance()
                return Token(MOD, '%', self.pos-1)

            if self.current_char == '^':
                self.advance()
                return Token(POW, '^', self.pos-1)

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(', self.pos-1)

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')', self.pos-1)
            
            self.error()
        
        raise StopIteration

