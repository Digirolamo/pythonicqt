"""File contains base class/metaclass for examples.
Auto collects imported examples so the example editor can easily find them."""
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
            if cls.__module__ in MetaExample.all_examples:
                first_name = MetaExample.all_examples[cls.__module__].__name__
                second_name = cls.__name__
                raise TypeError("Only one item can inherit from ExampleBase per module."
                               " Issue with {} and {} in {}.".format(first_name, second_name, cls.__module__))
            MetaExample.all_examples[cls.__module__] = cls
        return type(QtCore.Qt).__init__(cls, name, bases, dct)

class ExampleBase(QtGui.QGroupBox):
    """Having a base example class allows us to extend examples in the future.
    Only one class can inherit from this class in each module."""
    __metaclass__ = MetaExample
    #override these class attributes.
    title = "Untitled"

    def __init__(self, *args, **kwargs):
        super(ExampleBase, self).__init__(title=self.title, *args, **kwargs)


