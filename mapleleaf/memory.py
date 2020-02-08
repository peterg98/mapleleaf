class Memory(dict):
    def __init__(self, outer=None):
        self.outer = outer

    def get(self, name):
        if name in self:
            return self[name]
        # Recursively retrieve the variable in outer scopes
        if self.outer is not None:
            return self.outer.get(name)
        
        raise RuntimeError("%s is not defined." % name)

    def assign(self, name, value):
        if name in self:
            self[name] = value
            return
        if self.outer is not None:
            self.outer.assign(name, value)
            return
        raise RuntimeError("%s was not initialized." % name)

    def define(self, name, value):
        self[name] = value

