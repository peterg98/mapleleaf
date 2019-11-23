import lexer

error = False

def report_error(line_number, message):
    print("Error has occured at line {0}: {1}".format(line_number, message))
    error = True

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
    for token in tokens:
        print(token)

if __name__ == "__main__":
    run_file("sample.maple")
