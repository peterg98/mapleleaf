from abc import ABC

class Statement(ABC):
    pass

class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

class Expression(Statement):
    def __init__(self, expression):
        self.expression = expression

class Print(Statement):
    def __init__(self, expression):
        self.expression = expression

class VariableInitializer(Statement):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer