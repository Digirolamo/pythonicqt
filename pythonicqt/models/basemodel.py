"""This module contains the BaseModel class """
import copy
import six
from pythonicqt.Qt import QtCore
from pythonicqt.baseclasses import QtMetaStitch
from pythonicqt.models.modelitems import ItemContainer


@six.add_metaclass(QtMetaStitch)
class _BaseModel(object):
    """An implimentation of compatable QAbstractItemModel methods for subclasses.

        This class is a partial implimentation of the abstract interface for item model classes.
        This is a partial implimentation meant to be subclassed, it is used for common methods
        and to uphold DRY.

    Keyword Args:
        container (Optional[list]): The first parameter is a list if you want to instantiate
            an instance with starting values. If provided, a copy of the list is created.
        item_factory(object): A class that impliments the __getitem__ and __setitem__
    """
    default_data = {
        QtCore.Qt.ItemFlags: 
            (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | 
             QtCore.Qt.ItemIsDragEnabled |  QtCore.Qt.ItemIsSelectable)
        }


        
    def rowCount(self, parent=None):
        """Returns the length of the underlying list.
        Note:
            This method overrides the virtual function of it's parent.
        """
        if parent is None:
            return 0
        return len(self._container)
    
