# main.py
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def run_interpreter(code: str):
    print("\nRunning program:")
    print("---------------")
    print(code)
    print("---------------")
    print("Output:")
    
    lexer = Lexer(code)
    parser = Parser(lexer)
    interpreter = Interpreter()
    
    try:
        ast = parser.program()
        interpreter.interpret(ast)
    except Exception as e:
        print(f"Error: {e}")
    print()

def main():
    # Test Case 1: Basic arithmetic and printing
    program1 = """
    let x = 10 + 5;
    let y = x * 2;
    print(x);
    print(y);
    """
    run_interpreter(program1)

if __name__ == "__main__":
    main()