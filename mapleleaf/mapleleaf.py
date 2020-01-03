import lexer
import mapleparser
import interpreter

error = False
runtimeError = False

def token_error(token, message):
    if token.type == "EOF":
        report_error(token.line, "Error at end")
    else:
        report_error(token.line, " at '{0}' {1}".format(token.lexeme, message))

def report_error(line_number, message):
    print("Error has occured at line {0}: {1}".format(line_number, message))
    error = True

def report_runtime_error(error):
    print("Runtime error with message: {1}".format(error.message))

def run_file(file):
    with open(file, 'rb') as f:
        run(f.read().decode('utf-8'))

def run_from_prompt():
    while True:
        line = input("mapleleaf > ")
        run(line)
        error = False

def run(source):
    lex = lexer.Lexer(source)
    tokens = lex.scan_tokens()

    parser = mapleparser.Parser(tokens)
    statements = parser.parse()

    interpret = interpreter.Interpreter()
    result = interpret.interpret(statements)

if __name__ == "__main__":
    run_file("sample.maple")
