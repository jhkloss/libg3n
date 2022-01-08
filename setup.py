from setuptools import setup

setup(name='libg3n',
      version='0.1',
      description='Library generation framework',
      url='http://github.com/jhkloss/libg3n',
      author='Jan Kloß',
      author_email='jan.kloss@fh-erfurt.de',
      license='MIT',
      packages=['libg3n', 'libg3n.exception', 'libg3n.model', 'libg3n.modules', 'libg3n.modules.python', 'libg3n.modules.java'],
      zip_safe=False)