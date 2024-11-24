import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

class InteractiveInterpreter:
    def __init__(self):
        self.interpreter = Interpreter()
        self.input_buffer = []
        self.expecting_indent = False

    def execute_line(self, line: str, show_prompt: bool = True) -> bool:
        # Skip empty lines
        if not line.strip():
            return True
            
        # Check for exit command
        if line.strip().lower() == 'exit':
            return False
            
        # Add semicolon if missing for non-block statements
        if not line.strip().endswith(':') and not line.strip().endswith(';'):
            line = line.strip() + ';'
            
        # Add line to buffer
        self.input_buffer.append(line)
            
        # Process complete statement
        try:
            # Combine all lines
            full_program = '\n'.join(self.input_buffer)
            
            lexer = Lexer(full_program)
            parser = Parser(lexer)
            ast = parser.program()
            self.interpreter.interpret(ast)
            
            # Print current variables if requested
            if full_program.strip().lower() == 'vars;':
                self.show_variables()
                
        except Exception as e:
            if show_prompt:
                print(f"Error: {e}")
            else:
                print(f"Error in program: {e}")
            
        # Clear the buffer after processing
        self.input_buffer = []
        self.expecting_indent = False
        return True
    
    def show_variables(self):
        print("\nCurrent variables:")
        for var, value in self.interpreter.variables.items():
            print(f"{var} = {value}")
            
    def execute_file(self, filename: str):
        try:
            with open(filename, 'r') as file:
                print(f"\nExecuting file: {filename}")
                print("---------------")
                lines = file.readlines()
                
                # Print the program
                print("Program:")
                for line in lines:
                    print(line.rstrip())
                print("\nOutput:")
                
                # Execute each line
                for line in lines:
                    if not self.execute_line(line, show_prompt=False):
                        break
                        
                # Show final variable state
                print("\nFinal variable state:")
                self.show_variables()
                
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error reading file: {e}")

def print_help():
    print("""
Simple Interpreter Usage:
    python main.py                 : Interactive mode
    python main.py -f <filename>   : Run program from file
    python main.py -h              : Show this help message

Interactive Mode Commands:
    exit    : Exit the interpreter
    vars;   : Show all current variables

Example:
    python main.py -f program.txt
    """)

def interactive_mode():
    print("Simple Interpreter Interactive Mode")
    print("Commands:")
    print("  exit    - Exit the interpreter")
    print("  vars;   - Show all variables")
    print("Example:")
    print("  let x = 5;")
    
    interpreter = InteractiveInterpreter()
    
    while True:
        try:
            # Show different prompt when collecting block input
            prompt = '... ' if interpreter.input_buffer else '>>> '
            line = input(prompt)
            if not interpreter.execute_line(line):
                break
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            interpreter.input_buffer = []
            interpreter.expecting_indent = False
            continue
        except EOFError:
            break

def main():
    if len(sys.argv) == 1:
        # No arguments - enter interactive mode
        interactive_mode()
    elif len(sys.argv) >= 2:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print_help()
        elif sys.argv[1] == '-f' and len(sys.argv) == 3:
            # File mode
            interpreter = InteractiveInterpreter()
            interpreter.execute_file(sys.argv[2])
        else:
            print("Invalid arguments.")
            print_help()

if __name__ == "__main__":
    main()