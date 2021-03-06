import ast

from libg3n.model.libg3n_class import Libg3nClass
from libg3n.modules.python.python_codegen import to_source


class PythonClass(Libg3nClass):

    @property
    def file_extension(self) -> str:
        return 'py'

    def glue_properties(self):
        result = []
        for property in self._properties.values():
            result.append(property.to_ast())
        return result

    def to_ast(self):
        class_definition = ast.ClassDef(self._name, decorator_list=[], bases=[])
        # Add Meta class
        if self._meta_class:
            class_definition.bases.append(ast.Name(self._meta_class, ctx=ast.Load()))
        #TODO: meta_class Import
        class_definition.body = self.glue_properties()
        return ast.Module(body=[class_definition])

    def to_code(self) -> str:
        class_ast = self.to_ast()
        return to_source(class_ast)
