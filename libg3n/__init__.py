import logging

from libg3n.modules.python.python_decorators import generate
from libg3n.modules.python.python_codegen import to_source
from .generator import Generator

# Configure the Logger
logger = logging.getLogger('libg3n_logger')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s - %(levelname)s : %(asctime)s : %(message)s ')

stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)