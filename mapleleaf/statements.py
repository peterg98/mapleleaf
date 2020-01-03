from abc import ABC

class Statement(ABC):
    def execute(self):
        pass

class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

# class Expression(Statement):
#     def __init__(self, expression):
#         self.expression = expression

#     def execute(self):
#         self.expression.evaluate()

class Print(Statement):
    def __init__(self, expression):
        self.expression = expression

    def execute(self):
        value = str(self.expression.evaluate())
        print(value)

class VariableInitializer(Statement):
    def __init__(self, name, initializer, environment):
        self.name = name
        self.initializer = initializer
        self.environment = environment

    def execute(self, statement):
        value = None
        if self.initializer is None:
            value = self.initializer.evaluate()
        self.environment[name] = value