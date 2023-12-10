""""
This Is the main program.
"""

from calc.evaluator import evaluate

PROMPT = '\033[32m\033[0m '

def main():
    while True:
        try:
            print(evaluate(input(PROMPT).strip()))
        except EOFError:
            break
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
