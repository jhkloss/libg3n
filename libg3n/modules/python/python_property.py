import ast
from libg3n.model.libg3n_property import Libg3nProperty


class PythonProperty(Libg3nProperty):

    def to_ast(self):
        assignment = ast.Assign()
        assignment.targets = [ast.Name(id=self._name, ctx=ast.Store())]
        assignment.value = ast.Constant(value=self._value)
        return assignment
