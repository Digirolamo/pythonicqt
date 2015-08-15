"""File contains base class/metaclass for examples."""
from collections import OrderedDict
from PySide import QtCore, QtGui

class MetaExample(type(QtCore.Qt)):
    """Stores subclasses in a OrderedDict for easy collection.
    all_examples starts as None, but becomes and OrderedDict
    mapping module to example"""
    all_examples = None
    def __init__ (cls, name, bases, dct):
        #Create the list and don't add the base for the first base example.
        if MetaExample.all_examples is None:
            MetaExample.all_examples = OrderedDict()
        else:
            MetaExample.all_examples[cls.__module__] = cls
        return type(QtCore.Qt).__init__(cls, name, bases, dct)

class ExampleBase(QtGui.QGroupBox):
    """Having a base example class allows us to extend examples in the future."""
    __metaclass__ = MetaExample
    #override these class attributes.
    title = "Untitled"

    def __init__(self, *args, **kwargs):
        super(ExampleBase, self).__init__(title=self.title, *args, **kwargs)


