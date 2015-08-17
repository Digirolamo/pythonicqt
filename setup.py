import os
import json

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version_path = os.path.join("pythonicqt", "_version.py")
with open(version_path) as f:
    version = json.load(file)

packages = [
    'pythonicqt',
    'pythonicqt.tests',
    'pythonicqt.examples',
    'pythonicqt.models',
    'pythonicqt.widgets',
]

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

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
    install_requires=['PySide>=1.2.1', 'pytest'],
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
    
