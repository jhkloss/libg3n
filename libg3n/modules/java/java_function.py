from libg3n.model.libg3n_function import Libg3nFunction, FunctionType


class JavaFunction(Libg3nFunction):

    _start_line: int
    _end_line: int

    @property
    def start_line(self) -> int:
        return self._start_line

    @property
    def end_line(self) -> int:
        return self._end_line

    @start_line.setter
    def start_line(self, start_line: int):
        self._start_line = start_line

    @end_line.setter
    def end_line(self, end_line: int):
        self._end_line = end_line

    def _return_function_body(self) -> any:
        pass

    def _custom_function_body(self) -> any:
        pass

    def _external_function_body(self) -> any:
        pass