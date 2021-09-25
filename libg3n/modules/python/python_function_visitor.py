import ast
import libg3n
import python_decorators
from libg3n.modules.python.python_file import PythonFile


class PythonFunctionVisitor(ast.NodeVisitor):
    __loaded_functions: dict
    __current_file: PythonFile

    def load_functions(self, functions: dict):
        self.__loaded_functions = functions

    def set_current_file(self, file: PythonFile):
        self.__current_file = file

    def __get_function_by_ident(self, ident: str):
        func = None

        # Match ident with config function dict
        if ident in self.__loaded_functions:
            libg3n.logger.debug('Found matching config value for decorator id ' + ident)
            # Get the right function
            func = self.__loaded_functions[ident]
        return func

    def __refactor_function(self, ident, node) -> bool:
        success = False

        # Find and validate Function
        func = self.__get_function_by_ident(ident)
        if func:
            function_body = func.generate_body()
            # Perform the refactoring
            # TODO: AST Validation
            if function_body:
                node.body = function_body
                # Touch the file so we know it was altered and needs to be recompiled
                self.__current_file.touch()
                success = True
        return success

    def visit_FunctionDef(self, node):
        for decorator in node.decorator_list:
            # Confirm decorator structure
            if isinstance(decorator, ast.Call):
                # Get decorator name
                decorator_name: str = self._get_decorator_id(decorator)
                # Check if decorator is used by libg3n
                if decorator_name and self._is_libg3n_decorator(decorator_name):

                    libg3n.logger.debug(
                        'Found libg3n decorator in ' + self.__current_file.path + ' in line ' + str(node.lineno - 1))

                    # Get and validate the ident arg
                    # TODO: Outsource to helper.py
                    if isinstance(decorator.args[0], ast.Constant):
                        ident = decorator.args[0].__getattribute__('value')

                        self.__refactor_function(ident, node)

    @staticmethod
    def _get_decorator_id(decorator: ast.Call):
        decorator_id: str = ''

        # Get decorator name
        decorator_function: ast.Name = decorator.__getattribute__('func')

        if isinstance(decorator_function, ast.Name):
            decorator_id = decorator_function.__getattribute__('id')
            assert decorator_id != '', 'Decorator id could not be extracted. Wrong structure?'

        return decorator_id

    # Check if decorator is used by libg3n
    @staticmethod
    def _is_libg3n_decorator(identifier: str):
        found = False
        # TODO: Make this dynamic
        if identifier == python_decorators.generate.__name__:
            found = True

        return found
