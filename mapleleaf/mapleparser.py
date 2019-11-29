import mapleleaf
from errors import *
from expressions import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except ParseError as err:
            return None

    def expression(self):
        return self.equality()

    def equality(self):
        left = self.comparison()
        while self.match("DOUBLE_EQUAL", "BANG_EQUAL"):
            operator = self.previous()
            right = self.comparison()
            left = BinaryExp(left, operator, right)
        return left

    def comparison(self):
        left = self.addition()
        while self.match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = self.previous()
            right = self.addition()
            left = BinaryExp(left, operator, right)
        return left

    def addition(self):
        left = self.multiplication()
        while self.match("PLUS", "MINUS"):
            operator = self.previous()
            right = self.multiplication()
            left = BinaryExp(left, operator, right)
        return left

    def multiplication(self):
        left = self.unary()
        while self.match("SLASH", "STAR"):
            operator = self.previous()
            right = self.unary()
            left = BinaryExp(left, operator, right)
        return left

    def unary(self):
        if self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.terminal()

    def terminal(self):
        if self.match("FALSE"):
            return Literal(False)
        if self.match("TRUE"):
            return Literal(True)
        if self.match("NIL"):
            return Literal(None)
        if self.match("NUMBER", "STRING"):
            return Literal(self.previous().literal)
        if self.match("LEFT_PAREN"):
            expr = self.expression()
            self.consume("RIGHT_PAREN", "Expected a )")
            return Group(expr)

    def match(self, *args):
        for token_type in args:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self):
        self.current += 1
        return self.previous()

    def previous(self):
        return self.tokens[self.current-1]

    def peek(self):
        return self.tokens[self.current]

    def error(self, token, message):
        mapleleaf.token_error(token, message)
        return ParseError()

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)

    def is_at_end(self):
        return self.peek().type == "EOF"

    #skip to the next valid starting point of an expression
    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == "SEMICOLON": return
            if self.peek().type in ["CLASS", "FUNCTION", "VAR", "FOR", "IF", "WHILE", "PRINT", "RETURN"]:
                return
            self.advance()
    