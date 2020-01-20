from token import Token
import mapleleaf

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {x: x.upper() for x in [
            "and", "class", "else", "false", "from", "fun", "if",
            "nil", "or", "print", "return", "super", "this", "true",
            "var", "until"
        ]}

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens

    def advance(self):
        self.current += 1
        return self.source[self.current-1]

    def scan_token(self):
        char = self.advance()
        if char == "(": self.add_token("LEFT_PAREN")
        elif char == ")": self.add_token("RIGHT_PAREN")
        elif char == "{": self.add_token("LEFT_BRACE")
        elif char == "}": self.add_token("RIGHT_BRACE")
        elif char == ",": self.add_token("COMMA")
        elif char == ".": self.add_token("DOT")
        elif char == "-": self.add_token("MINUS")
        elif char == "+": self.add_token("PLUS")
        elif char == ";": self.add_token("SEMICOLON")
        elif char == "*": self.add_token("STAR")
        elif char == "/": self.add_token("SLASH")
        elif char == "!": self.add_token("BANG_EQUAL" if self.match("=") else "BANG")
        elif char == "=": self.add_token("DOUBLE_EQUAL" if self.match("=") else "EQUAL")
        elif char == "<": self.add_token("LESS_EQUAL" if self.match("=") else "LESS")
        elif char == ">": self.add_token("GREATER_EQUAL" if self.match("=") else "GREATER")
        elif char == "#":
            while self.peek() != "\n" and not self.is_at_end():
                self.advance()
        elif char == '"': self.string()
        elif char.isspace(): return
        else:
            if char.isdigit():
                self.number()
            elif char.isalpha():
                self.identifier()
            else:
                mapleleaf.report_error(self.line, "Invalid character for identifier.")


    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected):
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end(): return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source): return "\0"
        return self.source[self.current+1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n": self.line += 1
            self.advance()
        
        #call this when string does not have a closing double quote
        if self.is_at_end():
            mapleleaf.report_error(self.line, "Unterminated string.")
            return

        #Advance to the closing "
        self.advance()

        value = self.source[self.start+1:self.current-1]
        self.add_token("STRING", value)

    def number(self):
        while self.peek().isdigit():
            self.advance()
        #Look for the fractional part of the number
        if self.peek() == "." and self.peek_next().isdigit():
            #Skip the decimal
            self.advance()
            
            while self.peek().isdigit():
                self.advance()
        self.add_token("NUMBER", float(self.source[self.start:self.current]))
    
    def identifier(self):
        while self.peek().isalnum():
            self.advance()
        value = self.source[self.start:self.current]
        if value not in self.keywords:
            self.add_token("IDENTIFIER")
        else:
            self.add_token(self.keywords[value])