from libg3n.model.libg3n_regex_parser import Libg3nRegexParser


class JavaRegexParser(Libg3nRegexParser):

    @property
    def regex_body(self) -> str:
        return '{' + self.regex_spacer + 'return' + self.regex_spacer + '(.*)' + self.regex_spacer + ';' + self.regex_spacer + '}'

    @property
    def regex_modificator(self) -> str:
        # Define Java function modificators
        java_mod_token = ['private', 'public', 'protected', 'abstract']

        # Glue modificators to regex
        glued_java_mod_token = self.glue_regex_token_list(java_mod_token)

        # Add group and return
        return self._add_regex_group(glued_java_mod_token, self.GroupNames.MODIFICATOR)

    @property
    def regex_type(self) -> str:
        # Define Java function typs
        java_primitive_types = ['void', 'boolean', 'int', 'long', 'short', 'byte', 'float', 'double', 'char', 'String']

        # Glue types to regex
        glued_java_primitive_types = self.glue_regex_token_list(java_primitive_types)

        # Add group and return
        return self._add_regex_group(glued_java_primitive_types, self.GroupNames.TYPE)

    @property
    def regex_sig(self) -> str:
        return self._add_regex_group(r'\w+\(.*\)', self.GroupNames.SIGNATURE)

    @property
    def regex_string(self) -> str:
        return self.regex_annotation + self.regex_spacer + self.regex_modificator + self.regex_spacer + self.regex_type \
               + self.regex_spacer + self.regex_sig + self.regex_spacer + self.regex_body