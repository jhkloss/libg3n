from enum import IntEnum, unique, auto
# Define the function type strings as used in the configuration.

# Marks a function to be generated using the code generator.
# The ident parameter is used to match a function with the configuration.
# The type parameter is used to shortcut certain function types.
def generate(ident):
    assert ident != None, 'The generate decorater must specify an identifier!'
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return wrapper
