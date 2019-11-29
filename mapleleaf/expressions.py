from abc import ABC
from numbers import Number

def is_true(expr):
    if expr == None: return False
    if type(expr) == bool: return expr
    if type(expr) == int or type(expr) == float: return expr == 0
    if type(expr) == str: return expr == ""
    return True

def is_equal(left, right):
    if left is None is right == None: return True
    if left is None or right is None: return False
    return left == right

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
        if self.operator.type == "MINUS":
            if (isinstance(left, Number) and isinstance(right, Number)):
                return left - right
            if isinstance(left, str) and isinstance(right, str):
                if len(right) > len(left):
                    raise RuntimeError("Length of second string is greater than the first string.")
                #Implement KMP algorithm here
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
