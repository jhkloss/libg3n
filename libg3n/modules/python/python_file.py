from ast import parse, fix_missing_locations
from libg3n.modules.python.python_codegen import to_source
from libg3n.modules.python.python_function_visitor import PythonFunctionVisitor
from libg3n.model.libg3n_file import Libg3nFile
from libg3n.model.libg3n_config import Libg3nConfig


class PythonFile(Libg3nFile):

    _visitor = PythonFunctionVisitor()
    _tree: any

    @property
    def file_extension(self) -> str:
        return 'py'

    def parse(self):
        # Check if path is set and file exists

        file_contents = self.read()
        if file_contents:
            ast_tree = parse(file_contents)
            self._tree = ast_tree
            return ast_tree

    def process(self, config: Libg3nConfig):
        # Load ast Visitor with current file
        self._visitor.set_current_file(self)

        # Load ast Visitor with config functions
        self._visitor.load_functions(config.functions)

        # Visit AST nodes of the current file and perform our manipulations
        self._visitor.visit(self._tree)

    def unparse(self) -> str:
        # Fix line numbers
        fix_missing_locations(self._tree)

        # Unparse
        code = to_source(self._tree)
        self._code = code
        return code
