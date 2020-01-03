import mapleleaf
from memory import Memory

class Interpreter:
    memory = Memory()
    def interpret(self, statements):
        try:
            for statement in statements:
                statement.execute()
        except RuntimeError as e:
            mapleleaf.report_runtime_error(e)