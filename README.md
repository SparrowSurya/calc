# Calculator 

[![App running state](https://img.shields.io/badge/status-WIP-lighgrey)]()
[![Language used](https://img.shields.io/badge/python-3.11-blue)]()
[![External dependies used](https://img.shields.io/static/v1?label=dependencies&message=None&color=lightgrey)]()

**Work In Progress**

Calculator made in python with no dependencies.


---
### How to run
__file__: `main.py`

In terminal run:
```ps1
python main.py
```


---

### Grammar
Syntax -
```
expr   : term
       | (PLUS | MINUS) expr

exprs  : expr 
       | COMMA exprs

term   : factor 
       | (MUL | DIV | MOD | POW) term

factor : num
       | LPAREN expr RPAREN
       | (PLUS | MINUS) term
       | NAME<function> LPAREN exprs RPAREN  
       | NAME<constant>

num    : INT
       | FLOAT
```
---

### Definitions
Here is Regular Expressions for tokens.
```
NAME   = '[a-zA-Z][a-A-Z0-9]*'
INT    = '[+-]?[0-9]+(e[+-]?[0-9]+)?'
FLOAT  = '[+-]?[0-9]+([.][0-9]+)(e[+-]?[0-9]+)?'
LPAREN = '('
RPAREN = ')'
PLUS   = '+'
MINUS  = '-'
MUL    = '*'
DIV    = '/'
MOD    = '%'
POW    = '^'
```

### Using Lexer
It takes input expression and tokenises it.
Here are few ways to do it.

Example:

```py
tokens = [token for token in Lexer('2+3')]
```
OR
```py
lex = Lexer('2+3')
tokens = lex.tokenise()
```

### Using Parser
It takes in the tokens from lexer and builds a tree of nodes.

Example:

```py
p = Parser([token for token in Lexer('2+3')])
tree = p.parse()
```

### Using Interpreter
It takes the node tree from parser and evaluates it.

Example:

```py
p = Parser([token for token in Lexer('2+3')])
value = Interpreter(p.parse())
```

