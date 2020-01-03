class Parent:
    memory = [1, 2, 3, 4, 5]

class Child(Parent):
    def __init__(self, context):
        self.tmp_env = context.memory
        self.block_env = [2, 3, 4, 5, 6]
        self.context = context
        context.memory = self.block_env

    def rollback(self):
        self.block_env.append(7)
        self.context.memory = self.tmp_env


p = Parent()
c = Child(p)

c.rollback()