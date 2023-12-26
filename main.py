""""
This Is the main program.
"""

from calc.evaluator import evaluate

PROMPT = '\033[32m\033[0m '

def main():
    print("Enter 'CTRL+Z' to exit!", end='\n\n')
    while True:
        try:
            print(evaluate(input(PROMPT).strip()))
        except EOFError:
            break
        except KeyError as e:
            print(f"NameError: {e} is not defined")
        except Exception as e:
            print(f"{type(e).__name__}:", e)

if __name__ == '__main__':
    main()
