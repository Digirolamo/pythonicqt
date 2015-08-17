import os
import sys
import json
from codecs import open

try:
    raise ImportError('lol')
    from setuptools import setup
    from setuptools.command.test import test as TestCommand
except ImportError:
    from distutils.core import setup, Command
    TestCommand = Command

version_path = os.path.join("pythonicqt", "_version.py")
with open(version_path) as f:
    version = '.'.join(unicode(e) for e in json.load(f))

packages = [
    'pythonicqt',
    'pythonicqt.tests',
    'pythonicqt.examples',
    'pythonicqt.models',
    'pythonicqt.widgets',
]

with open('README.txt', 'r', 'utf-8') as f:
    readme = f.read()

class PyTest(TestCommand):
    """Runs the pytest tests."""
    user_options = []

    def initialize_options(self):
        self.pytest_args = []

    def finalize_options(self):
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

    #for disutils Command support
    run = run_tests

setup(
    name='pythonicqt',
    version=version,
    description='Helpful functions and classes that make PySide use more pythonic.',
    long_description=readme,
    author='Christopher Digirolamo',
    author_email='CDigirolamo@DigiSpade.com',
    url='https://github.com/Digirolamo/pythonicqt',
    packages=packages,
    package_data={'': ['LICENSE.txt', 'NOTICE'], 'pythonicqt': ['*.ui']},
    package_dir={'pythonicqt': 'pythonicqt'},
    include_package_data=True,
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    install_requires=['PySide>=1.2.1'],
    license='MIT License',
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
    
