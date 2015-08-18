"""This module contains the Data structures and classes
that are used to impliment a python list like QAbstractListmodel.
"""
from six.moves import xrange
from PySide import QtCore


class ItemMetaData(dict):
    """Contains flags and roles"""


class ListModel(QtCore.QAbstractListModel):
    """A python list implimentation of a QAbstractListModel.

    Instances of this class function as both a QAbstractListModel and
    a python list. This allows you to interact with the object like any
    other python list through convenient methods and index access, but
    with the benifit of updating all connected views. The connected
    Qt views can also edit and change the list.

    Note:
        This object emits two signals in addition to the signals emited by
        QAbstractListModel.
        ListChanged (Signal(int, object)): A Qt Signal that emits when a value at
            an index in the list changes. Emits the index and previous value changed.
        ListCleared (Signal()): Emited when the list is cleared.

    Attributes:
        default_flags (ItemFlag): The default flags that all of the items return.
            Change an instance variable of the same name, or subclass this class
            and redefine this attribute if you want to use different flags.
        default_roles (dict[ItemRole]): The default roles that all of the items return.

    Args:
        container (Optional[list]): The first parameter is a list if you want to instantiate
            an instance with starting values. If provided, a copy of the list is created.
    """
    ListChanged = QtCore.Signal(int, object) 
    ListCleared = QtCore.Signal() 

    default_flags = (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | 
                     QtCore.Qt.ItemIsDragEnabled |  QtCore.Qt.ItemIsSelectable)
    default_roles = {}

    def __init__(self, container=None):
        QtCore.QAbstractListModel.__init__(self)
        if container is None:
            container = []
        self._container = container
        self.container_meta = [ItemMetaData() for e in range(len(container))] #index to role/flag index
        
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """Class methods are similar to regular functions.

        Note:
            This method overrides the virtual function of it's parent.
        """

        if orientation == QtCore.Qt.Vertical:
            return unicode(section)
        else:
            return unicode(section)

    def rowCount(self, parent=None):
        """Returns the length of the underlying list.

        Note:
            This method overrides the virtual function of it's parent.
        """
        if parent is None:
            return 0
        return len(self._container)
    
    def columnCount(self, parent=None):
        """Returns 1 because lists do not have multiple columns.

        Note:
            This method overrides the virtual function of it's parent.
        """
        return 1
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Returns the data of a role at a specific index of the list.

        If the role is DisplayRole or EditRole, returns the value located
        in the underlying list at the index. Else returns the role of the
        individual item if the user has set it. Else returns the default
        role data located in the class attribute if it exists.

        Args:
            index (QModelIndex):
            role (Optional[ItemRole]):

        Note:
            This method overrides the virtual function of it's parent.
        """
        if not index.isValid():
            return None
        row, column = index.row(), index.column()
        if role == QtCore.Qt.DisplayRole:
            return unicode(self._container[row])
        item_metadata = self.container_meta[row]
        try:
            return item_metadata[role]
        except KeyError as e:
            return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """Sets the data of a role at a specific index of the list.

        If the role is DisplayRole or EditRole, sets the value located
        in the underlying list at the index. Else sets the role of the
        individual item specifically.

        Args:
            index (QModelIndex):
            role (Optional[ItemRole]):

        Note:
            This method overrides the virtual function of it's parent.
        """
        if not index.isValid():
            return None
        row, column = index.row(), index.column()
        if role == QtCore.Qt.EditRole:
            self[row] = value
            return True
    
    def flags(self, index):
        """If no specific flags exist for an item, returns the default
        flags of attribute self.default_flags.
        
        Note:
            This method overrides the virtual function of it's parent.
        """
        row = index.row()
        item_metadata = self.container_meta[row]
        try:
            return item_metadata.flags
        except (KeyError, AttributeError):
            pass
        return self.default_flags

    #TODO
    def set_default_meta(self, role, value):
        """"""
        
    def set_meta(self, idx, role, value):
        """Returns a list that"""
        self.container_meta[idx][role] = value
        index = self.index(idx, 0)
        self.dataChanged.emit(index, index)

    # Python Special Methods

    def __str__(self):
        """Returns the __str__ of the underlying list."""
        return self._container.__str__()
    
    def __repr__(self):
        """The representation of the object, does not include any of the metadata
        such as flags and roles."""
        class_name = self.__class__.__name__
        list_repr = self._container.__repr__()
        return "{}({})".format(class_name, list_repr)

    def __eq__(self, *args):
        """Returns whether the underlying list equals another list."""
        return self._container.__eq__(*args)

    def __ne__(self, *args):
        """Returns whether the underlying list is not equal to another list."""
        return self._container.__ne__(*args)

    # Python Sequence Methods
    def __len__(self, *args):
        """Returns the length of the underlying list."""
        return self._container.__len__(*args)
    
    def __contains__(self, *args):
        """Returns whether or not an item is in the underlying list."""
        return self._container.__contains__(*args)
    
    def _convert_idx(self, idx):
        """To be compatable with Qt objects, ensure the index is a positive number.
        Used for python index operations."""
        if idx < 0:
            #idx -1 on a length 10 list is the same as idx 9 (10 + -1)
            idx = len(self) + idx
        return idx

    def __getitem__(self, idx):
        idx = self._convert_idx(idx)
        return self._container.__getitem__(idx)

    def __setitem__(self, idx, value):
        idx = self._convert_idx(idx)
        previous = self._container[idx]
        ret_value = self._container.__setitem__(idx, value)
        index = self.index(idx, 0)
        self.dataChanged.emit(index, index)
        self.ListChanged.emit(idx, previous)
        return ret_value

    def __delitem__(self, idx):
        """Deletes an item from the underlying list and any associated metadata,
        then updates the model."""
        idx = self._convert_idx(idx)
        previous = self._container[idx]
        parent = QtCore.QModelIndex()
        self.beginRemoveRows(parent, idx, idx) 
        ret_value = self._container.__delitem__(idx)
        self.container_meta.__delitem__(idx)
        self.endRemoveRows()
        self.ListChanged.emit(idx, previous)
        return ret_value

    #TODO methods
    def __setslice__ (self, *args):
        """We disable slice setting until we can handle
        alerting the datamodel of the changes"""
        raise NotImplementedError("No slice setting functionality.")
        
    def __delslice__ (self, *args):
        """We disable slice deleting until we can handle
        alerting the datamodel of the changes"""
        raise NotImplementedError("No slice deleting functionality.")


    #Reimplimenting popular python list methods.
    def remove(self, item):
        """Removes the first occurence of an item."""
        idx = self._container.index(item)
        del self[idx]

    def pop(self, idx=-1):
        """Takes an item at the 'idx' index from the list and returns it."""
        item_to_remove = self._container[idx]
        del self[idx]
        return item_to_remove

    def clear(self):
        """Clears entire model and emits layout changed"""
        self.layoutAboutToBeChanged.emit()
        self._container = self._container[:]
        self.layoutChanged.emit()
        self.ListCleared.emit()

    def insert(self, idx, value):
        previous = None
        try:
            previous = self._container[idx]
        except IndexError:
            pass
        parent = QtCore.QModelIndex()
        self.beginInsertRows(parent, idx, idx)
        ret_value = self._container.insert(idx, value)
        self.container_meta.insert(idx, ItemMetaData())
        self.endInsertRows()
        self.ListChanged.emit(idx, previous)
        return ret_value

    def append(self, value):
        return self.insert(len(self._container), value)

    def get_list(self):
        """Returns a new python list version of the container."""
        return list(self._container)