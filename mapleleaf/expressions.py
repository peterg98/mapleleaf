from abc import ABC
from numbers import Number
from utils import *
import interpreter

class Expression(ABC):
    def evaluate(self):
        pass

class BinaryExp(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if self.operator.type == "PLUS":
            if (isinstance(left, Number) and isinstance(right, Number)) or (isinstance(left, str) and isinstance(right, str)):
                return left + right
            elif (isinstance(left, str) and isinstance(right, Number)) or (isinstance(left, Number) and isinstance(right, str)):
                return str(left) + str(right)
        if self.operator.type == "MINUS":
            if (isinstance(left, Number) and isinstance(right, Number)):
                return left - right
            
            # Removes the first occurence of right from left, if it is present
            if isinstance(left, str) and isinstance(right, str):
                if len(right) > len(left):
                    raise RuntimeError("Length of second string is greater than the first string.")
                # Implement KMP algorithm later, but for now, do it the obvious way
                start = left.find(right)
                if start != -1:
                    return left[0:start] + left[start+len(right):]
                return left
        if self.operator.type == "GREATER":
            if isinstance(left, Number) and isinstance(right, Number):
                return left > right
        if self.operator.type == "GREATER_EQUAL":
            if isinstance(left, Number) and isinstance(right, Number):
                return left >= right
        if self.operator.type == "LESS":
            if isinstance(left, Number) and isinstance(right, Number):
                return left < right
        if self.operator.type == "LESS_EQUAL":
            if isinstance(left, Number) and isinstance(right, Number):
                return left <= right
        if self.operator.type == "DOUBLE_EQUAL":
            return left == right
        if self.operator.type == "SLASH":
            if isinstance(left, Number) and isinstance(right, Number):
                return left / right
        if self.operator.type == "STAR":
            if isinstance(left, Number) and isinstance(right, Number):
                return left * right
            if (isinstance(left, int) and isinstance(right, str)) or (isinstance(left, str) and isinstance(right, int)):
                return left * right

class Group(Expression):
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self):
        return self.expression.evaluate()

class Literal(Expression):
    def __init__(self, value):
        self.value = value
        #If value is a whole number, cast it to an integer
        if isinstance(value, Number) and value % 1 == 0:
            self.value = int(value)

    def evaluate(self):
        return self.value

class Logical(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        if self.operator.type == "OR":
            # Short circuit and 
            if is_true(left): return left
        # If operator is AND and if lvalue is false, then short circuit and return lvalue
        else:
            if not is_true(left): return left
        return self.right.evaluate()

class Unary(Expression):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def evaluate(self):
        right = self.right.evaluate()
        if self.operator == "BANG":
            return not is_true(right)
        if self.operator == "MINUS" and isinstance(right, Number):
            return -right

class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        return interpreter.Interpreter.memory.get(self.name)

class Assignment(Expression):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def evaluate(self):
        value = self.value.evaluate()
        interpreter.Interpreter.memory.assign(self.name, value)
        return value