from libg3n.model.libg3n_property import Libg3nProperty


class JavaProperty(Libg3nProperty):

    # Property access modificator
    _access: str

    # Property type
    _type: str

    PROPERTY_TEMPLATE = '{access} {type} {name} = {value};'

    @property
    def access(self) -> str:
        return self._access

    @access.setter
    def access(self, access: str):
        self._access = access

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, type: str):
        self._type = type

    def to_code(self):
        return self.PROPERTY_TEMPLATE.format(access=self._access, type=self._type, name=self._name, value=self._value)
