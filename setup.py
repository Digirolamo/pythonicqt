import os
import sys
import json
from codecs import open

try:
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

with open('README', 'r', 'utf-8') as f:
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
    package_dir={
        'pythonicqt': 'pythonicqt',
        'pythonicqt.examples': 'pythonicqt\\examples'},
    # "''" means all packages.
    package_data={'': ['*.ui']},
    #Apparently if you set include_package_data to True
    #package_data is NOT included in sdist...
    #include_package_data=True,
    
    #For bsdist the manifest isn't used so we have to collect the license another way.
    data_files=[('', ['LICENSE.txt'])],

    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    install_requires=['PySide>=1.2.1, six>=1.8.0'],
    license='MIT License',
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',

    ),
)
    
