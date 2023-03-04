from evaluator.tokens import *
from evaluator.ast_ import * 

__all__ = ('Parser',)

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self._gen = iter(self.tokens)
        self.current_token = next(self._gen) # WARN: fails if no tokens
    
    # TODO: to provide better error description with cause
    def error(self):
        raise SyntaxError(f'Invalid Syntax while parsing token[{self.current_token}]')
    
    def eat(self, token_type):
        """Compare the `current_token.type` with the token_type parameter
        and if they match then `eat` the current token and assign the next
        token to the self.current_token otherwise raise an exception.        
        """
        if self.current_token.type != token_type:
            self.error()

        try:
            self.current_token = next(self._gen)
        except StopIteration:
            self.current_token = None

    def expr(self) -> Num | UnaryOp | FnCall | BinOp | Const:
        """
        expr:
        >>> term
        >>> (PLUS | MINUS) expr
        """
        node = self.term()

        while self.current_token != None and self.current_token.type in (PLUS, MINUS):
            op = self.current_token.value
            if self.current_token.type == PLUS:
                self.eat(PLUS)
            elif self.current_token.type == MINUS:
                self.eat(MINUS)
            else:
                self.error()

            node = BinOp(left=node, op=op, right=self.term())
        
        return node 

    def exprs(self) -> tuple[Num | UnaryOp | FnCall | BinOp | Const]:
        """
        exprs:
        >>> expr
        >>> COMMA exprs
        """
        nodes = [self.expr()]

        while self.current_token != None and self.current_token.type == COMMA:
            self.eat(COMMA)
            nodes.extend(self.exprs())

        return tuple(nodes)
    
    def term(self) -> Num | UnaryOp | FnCall | BinOp | Const:
        """
        term:
        >>> factor 
        >>> (MUL | DIV | MOD | POW) term
        """
        node = self.factor()

        while self.current_token != None and self.current_token.type in (MUL, DIV, MOD, POW):
            op = self.current_token.value
            if self.current_token.type == MUL:
                self.eat(MUL)
            elif self.current_token.type == DIV:
                self.eat(DIV)
            elif self.current_token.type == MOD:
                self.eat(MOD)
            elif self.current_token.type == POW:
                self.eat(POW)

            node = BinOp(left=node, op=op, right=self.factor())
        
        return node
    
    def factor(self) -> Num | UnaryOp | FnCall | Const:
        """
        factor:
        >>> num
        >>> LPAREN expr RPAREN
        >>> (PLUS | MINUS) factor
        >>> NAME<function> LPAREN exprs RPAREN
        >>> NAME<constant>
        """
        if self.current_token.type in (INTEGER, FLOAT):
            num = self.current_token.value
            self.eat(self.current_token.type)
            return Num(num)
        
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        
        if self.current_token.type in (PLUS, MINUS):
            op = self.current_token.value
            self.eat(self.current_token.type)
            return UnaryOp(op, self.factor())
        
        if self.current_token.type == NAME:
            name = self.current_token.value
            self.eat(NAME)

            if self.current_token.type == LPAREN:
                self.eat(LPAREN)
                node = FnCall(name, tuple(self.exprs()))
                self.eat(RPAREN)
                return node
            else:
                return Const(name)
        
        self.error()
        

    def parse(self) -> Expr:
        """
        expr:
        >>> term
        >>> (PLUS | MINUS) expr

        exprs:
        >>> expr
        >>> COMMA exprs

        term:
        >>> factor 
        >>> (MUL | DIV | MOD | POW) term

        factor:
        >>> num
        >>> LPAREN expr RPAREN
        >>> (PLUS | MINUS) factor
        >>> NAME<function> LPAREN exprs RPAREN
        >>> NAME<constant>

        num:
        >>> INT
        >>> FLOAT
        """
        expr = self.expr()
        if self.current_token != None:
            self.error()
        return Expr(expr)

