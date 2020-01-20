from abc import ABC
from utils import *
from memory import Memory
import interpreter

class Statement(ABC):
    def execute(self):
        pass

class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

    def execute(self):
        block_env = Memory()
        block_env.outer = interpreter.Interpreter.memory
        try:
            interpreter.Interpreter.memory = block_env
            for statement in self.statements:
                statement.execute()
        finally:
            interpreter.Interpreter.memory = block_env.outer

class Expression(Statement):
    def __init__(self, expression):
        self.expression = expression

    def execute(self):
        self.expression.evaluate()

class Print(Statement):
    def __init__(self, expression):
        self.expression = expression

    def execute(self):
        value = str(self.expression.evaluate())
        print(value)

class VariableInitializer(Statement):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def execute(self):
        value = None
        if self.initializer is not None:
            value = self.initializer.evaluate()
        interpreter.Interpreter.memory.define(self.name, value)

class If(Statement):
    def __init__(self, condition, then, _else):
        self.condition = condition
        self.then = then
        self._else = _else

    def execute(self):
        if is_true(self.condition.evaluate()):
            self.then.execute()
        elif self._else != None:
            self._else.execute()
    
class Until(Statement):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def execute(self):
        while is_true(self.condition.evaluate()):
            self.statement.execute()

class From(Statement):
    def __init__(self, initializer, condition):
        self.initializer = initializer
        self.condition = condition