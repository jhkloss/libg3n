from libg3n.model.libg3n_class import Libg3nClass


class JavaClass(Libg3nClass):
    CLASS_TEMPLATE = 'public class {name} {{\n {properties} }}'

    @property
    def file_extension(self) -> str:
        return 'java'

    def _unparse_properties(self) -> str:
        result = ''

        for property in self._properties:
            result += property.to_code()

        return result

    def to_code(self) -> str:
        return self.CLASS_TEMPLATE.format(name=self.name, properties=self._unparse_properties())
