import ast
from libg3n.model.libg3n_function import Libg3nFunction


class PythonFunction(Libg3nFunction):

    def _return_function_body(self) -> any:
        # TODO: Validate value
        return [ast.Return(ast.Constant(self.value))]

    def _custom_function_body(self) -> any:
        # TODO: Validate body
        return ast.parse(self._value).__getattribute__('body')

    def _external_function_body(self) -> any:
        with open(self._value) as f:
            file_content = f.read()
            return ast.parse(file_content)
