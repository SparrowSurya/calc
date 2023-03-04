from evaluator import *


def main() -> int | float:
    while True:
        print( Interpreter(func, const).eval(Parser([t for t in Lexer(input('calc> '))]).parse()) )


main()
