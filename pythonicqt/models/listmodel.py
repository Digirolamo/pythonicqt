"""
Data structures and class that acts like a python list and a Qt QListModel.
"""
from PySide import QtCore

class ItemMetaData(dict):
    """Contains flags and roles"""

class ListModel(QtCore.QAbstractListModel):
    #TODO DOCS
    """
    Signals Emited:
    ListChanged(int, object): the index changed, and the value before the change.
    ListCleared(): When the entire list is cleared. List Changed is not called in this case."""
    ListChanged = QtCore.Signal(int, object) 
    ListCleared = QtCore.Signal() 

    default_flags = (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | 
                     QtCore.Qt.ItemIsDragEnabled |  QtCore.Qt.ItemIsSelectable)
    default_roles = {}
    def __init__(self, container=None):
        QtCore.QAbstractListModel.__init__(self)
        if container is None:
            container = []
        self.container = container
        self.container_meta = [ItemMetaData() for e in xrange(len(container))] #index to role/flag index
        
    #QListModel virtual method
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Vertical:
            return unicode(section)
        else:
            return unicode(section)

    #QListModel virtual method
    def rowCount(self, parent=None):
        """Returns the length of the underlying list."""
        if parent is None:
            return 0
        return len(self.container)
    
    #QListModel virtual method
    def columnCount(self, parent=None):
        """Returns 1 because lists do not have multiple columns."""
        return 1
    
    #QListModel virtual method
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        row, column = index.row(), index.column()
        if role == QtCore.Qt.DisplayRole:
            return unicode(self.container[row])
        item_metadata = self.container_meta[row]
        try:
            return item_metadata[role]
        except KeyError as e:
            return None

    #QListModel virtual method  
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return None
        row, column = index.row(), index.column()
        if role == QtCore.Qt.EditRole:
            self[row] = value
            return True
    
    #QListModel virtual method
    def flags(self, index):
        """If no specific flags exist for an item, returns the default
        flags of attribute self.default_flags."""
        row = index.row()
        item_metadata = self.container_meta[row]
        try:
            return item_metadata.flags
        except (KeyError, AttributeError):
            pass
        return self.default_flags

    def set_default_meta(self, role, value):
        """"""
        
    def set_meta(self, idx, role, value):
        """Returns a list that"""
        self.container_meta[idx][role] = value
        index = self.index(idx, 0)
        self.dataChanged.emit(index, index)
    # Python Special Methods

    def __eq__(self, *args):
        """Returns whether this list equals another list."""
        return self.container.__eq__(*args)

    def __neq__(self, *args):
        """Returns whether this list is not equal to another list."""
        return self.container.__neq__(*args)

    # Python Sequence Methods
    def __len__(self, *args):
        return self.container.__len__(*args)
    
    def __contains__(self, *args):
        return self.container.__contains__(*args)
    
    def __delitem__(self, idx):
        idx = self._convert_idx(idx)
        previous = self.container[idx]
        parent = QtCore.QModelIndex()
        self.beginRemoveRows(parent, idx, idx) 
        ret_value = self.container.__delitem__(idx)
        self.container_meta.__delitem__(idx)
        self.endRemoveRows()
        self.ListChanged.emit(idx, previous)
        return ret_value

    def __getitem__(self, idx):
        idx = self._convert_idx(idx)
        return self.container.__getitem__(idx)

    def __setitem__(self, idx, value):
        idx = self._convert_idx(idx)
        previous = self.container[idx]
        ret_value = self.container.__setitem__(idx, value)
        index = self.index(idx, 0)
        self.dataChanged.emit(index, index)
        self.ListChanged.emit(idx, previous)
        return ret_value

    def _convert_idx(self, idx):
        """To be compatable with Qt objects, ensure the index is a positive number."""
        if idx < 0:
            #idx -1 on a length 10 list is the same as idx 9 (10 + -1)
            idx = len(self) + idx
        return idx

    def remove(self, item):
        """Removes the first occurence of an item."""
        idx = self.container.index(item)
        del self[idx]

    def pop(self, idx=-1):
        """Takes an item at the 'idx' index from the list and returns it."""
        item_to_remove = self.container[idx]
        del self[idx]
        return item_to_remove

    def clear(self):
        """Clears entire model and emits layout changed"""
        self.layoutAboutToBeChanged.emit()
        self.container = self.container[:]
        self.layoutChanged.emit()
        self.ListCleared.emit()

    def insert(self, idx, value):
        previous = None
        try:
            previous = self.container[idx]
        except IndexError:
            pass
        parent = QtCore.QModelIndex()
        self.beginInsertRows(parent, idx, idx)
        ret_value = self.container.insert(idx, value)
        self.container_meta.insert(idx, ItemMetaData())
        self.endInsertRows()
        self.ListChanged.emit(idx, previous)
        return ret_value

    def append(self, value):
        return self.insert(len(self.container), value)

    def get_list(self):
        """Returns a new python list version of the container."""
        return list(self.container)

    #TODO methods
    def __setslice__ (self, *args):
        """We disable slice setting until we can handle
        alerting the datamodel of the changes"""
        raise NotImplementedError("No slice setting functionality.")
        
    def __delslice__ (self, *args):
        """We disable slice deleting until we can handle
        alerting the datamodel of the changes"""
        raise NotImplementedError("No slice deleting functionality.")

    def __str__(self):
        return self.container.__str__()
    
    def __repr__(self):
        """The representation does not include any of the metadata."""
        sequence = self.container.__repr__()
        return "{}({})".format(self.__class__.__name__,
                                        sequence)