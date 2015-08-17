Note: We are still moving files over from a private repo into this repo. This project should not be relied upon until the migration is complete. As of 8/17/2015 20% has been moved here.
#PythonicQt
PythonicQt is an MIT licensed Python package that wraps and expands PySide to make development more Pythonic. 

Many classes in PySide do not fit a Pythonic paradigm. This package aims to subclass PySide classes and provide more python ways of using the classes. For example, having a context manager for the opening of a `QFile`. In addition to enhancing existing PySide classes, the package aims to provide new convenient boilerplate implementations of Models and Widgets. The `ListModel` is an example. A python-like list that is also a `QAbstractListWidget`.


##Planned/Implemented Features
Here are just a few planned and/or implemented features in PythonicQt:
  - ListModel: a convenient Python container implementation of a QAbstractListModel 
  - debounce: a decorator that debounces methods of QObjects using QTimers.

##Requirements
- [Python](https://www.python.org/downloads/): 2.7.x or 3.x
- [PySide](https://pypi.python.org/pypi/PySide): 1.2.1 or higher
- [six](https://pypi.python.org/pypi/PySide): 1.8.0 or higher
- [pytest](https://pypi.python.org/pypi/PySide): 2.6.1 or higher (for testing)

## Where to get it
Currently the source code is hosted at:
https://github.com/Digirolamo/pythonicqt
There will be a PyPi release after the package is more usable.

You can run the testing suite by running:
```sh
python setup.py test
```
or after installing the package running:
```sh
python -m pythonicqt.tests
```

## Quick Start

 You can view examples after installing the package by running:
```sh
python -m pythonicqt.examples
```

##Disclaimer
PySide is the Python Qt bindings project. PythonicQt is not affiliated with PySide or Qt.
