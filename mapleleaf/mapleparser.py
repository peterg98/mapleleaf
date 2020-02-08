import mapleleaf
from errors import *
from expressions import *
from statements import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []

        while not self.is_at_end():
            statements.append(self.statement())
        return statements

    def expression(self):
        return self.assignment()

    def declaration(self):
        try:
            if (self.match("VAR")):
                return self.var_declaration()
            return self.statement()
        except ParseError as e:
            self.synchronize()

    def statement(self):
        if self.match("UNTIL"):
            return self.until_statement()
        if self.match("FROM"):
            return self.from_statement()
        if self.match("IF"):
            return self.if_statement()
        if self.match("LEFT_BRACE"):
            return Block(self.block())
        if self.match("PRINT"):
            return self.print_statement()
        if self.match("VAR"):
            return self.var_declaration()
        return self.expression_statement()

    def from_statement(self):
        self.consume("LEFT_PAREN", "Expected a Left parenthesis")

        # Initializer was skipped, no initializer
        if self.match("SEMICOLON"):
            initializer = None
        # variable is declared
        elif self.match("VAR"):
            initializer = self.var_declaration()
        # Else, it must be an expression
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check("SEMICOLON"):
            condition = self.expression()
        
        self.consume("SEMICOLON", "Expected a ; after condition")

        increment = None
        if not self.check("RIGHT_PAREN"):
            increment = self.expression()
        self.consume("RIGHT_PAREN", "Expected a ) after from clause")
        body = Block([self.statement()])

        # If an increment exists, it is executed after the body
        if increment is not None:
            body.statements.append(Expression(increment))
        
        # If a condition does not exist, it is the same as a while loop
        if condition is None:
            condition = Literal(True)

        body = Until(condition, body)

        if initializer is not None:
            body = Block([initializer, body])

        return body

    def if_statement(self):
        self.consume("LEFT_PAREN", "Expected a '(' after 'if'.")
        condition = self.expression()
        self.consume("RIGHT_PAREN", "Expected a ')' after condition")

        then = self.statement()
        _else = None

        if (self.match("ELSE")):
            _else = self.statement()
        return If(condition, then, _else)

    def print_statement(self):
        value = self.expression()
        self.consume("SEMICOLON", "Expected a ; after print statement")
        return Print(value)

    def var_declaration(self):
        token = self.consume("IDENTIFIER", "Expected a variable name")
        initializer = None

        if (self.match("EQUAL")):
            initializer = self.expression()
        
        self.consume("SEMICOLON", "Expected a ; after declaration")
        return VariableInitializer(token.lexeme, initializer)

    def until_statement(self):
        self.consume("LEFT_PAREN", "Expected a ( after until.")
        condition = self.expression()
        self.consume("RIGHT_PAREN", "Expected a ) after condition")
        body = self.statement()

        return Until(condition, body)

    def expression_statement(self):
        expr = self.expression()
        self.consume("SEMICOLON", "Expected a ; after expression statement")
        return Expression(expr)

    def block(self):
        statements = []
        while not self.check("RIGHT_BRACE") and not self.is_at_end():
            statements.append(self.declaration())
        self.consume("RIGHT_BRACE", "Expected a } to end the block")
        return statements

    def assignment(self):
        expression = self._or()

        if self.match("EQUAL"):
            token = self.previous()
            value = self.assignment()

            if isinstance(expression, Variable):
                return Assignment(expression.name, value)
            
            token_error(token, "Expected an equals sign in variable assignment.")
        return expression

    def _or(self):
        left = self._and()

        while self.match("OR"):
            operator = self.previous()
            right = self._and()
            left = Logical(left, operator, right)
        return left

    def _and(self):
        left = self.equality()

        while self.match("AND"):
            operator = self.previous()
            right = self.equality()
            left = Logical(left, operator, right)
        
        return left

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
        if self.match("IDENTIFIER"):
            return Variable(self.previous().lexeme)
        if self.match("LEFT_PAREN"):
            expr = self.expression()
            self.consume("RIGHT_PAREN", "Expected a )")
            return Group(expr)
        if self.match("LEFT_BRACE"):
            return Block(self.block())

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
    