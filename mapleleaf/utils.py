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