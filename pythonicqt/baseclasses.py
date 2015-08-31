"""This module contains the base classes used by modules
throughout the pythonicqt package."""
from abc import ABCMeta
from pythonicqt.Qt import QtCore

class QtMetaStitch(ABCMeta, type(QtCore.QObject)):
    """In order to combine Qt types and object types we
    need to stitch the metaclasses together."""