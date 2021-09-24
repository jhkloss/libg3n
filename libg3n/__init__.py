import logging

from .decorators import generate
from libg3n.modules.python.python_config_parser import XMLParser
from libg3n.modules.python.python_codegen import to_source
from .generator import Generator
from .configuration import Configuration

# Configure the Logger
logger = logging.getLogger('libg3n_logger')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s - %(levelname)s : %(asctime)s : %(message)s ')

stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)