import mapleleaf

class Interpreter:
    def interpret(self, expression):
        try:
            result = expression.evaluate()
            print(result)
        except RuntimeError as e:
            mapleleaf.report_runtime_error(e)