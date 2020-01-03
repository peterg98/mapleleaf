class Memory(dict):
    def __init__(self, outer=None):
        self.outer = outer

    def __getitem__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        if self.outer is not None:
            return self.outer.__dict__[name]
        
        raise RuntimeError("%s is not defined." % name)

    def __setitem__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
        if self.outer is not None:
            self.outer.__dict__[name] = value

        raise RuntimeError("%s was not initialized." % name)

