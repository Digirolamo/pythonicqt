"""This module contains the class and data structures that make
the ListModel class.

"""

import six
from collections import MutableSequence
from pythonicqt.Qt import QtCore
from pythonicqt.baseclasses import QtMetaStitch
from pythonicqt.models.modelitems import ItemContainer

@six.add_metaclass(QtMetaStitch)
class BaseListModel(QtCore.QAbstractListModel):
    """"A working implimentation of QAbstractListModel.

    This class is a implimentation of the abstract interface of QAbstractListModel.
    self._container is an internal python list that holds the data of this
    QAbstractListModel. Internally, each value of the list is actually contained in
    instance of item_factory. The intention of thie class is to impliment the Qt
    QAbstractList model methods fully. 

    You can use this model as-is, but in pythonicqt the primary purpose is 
    the ListModel subclass of it.

    Keyword Args:
        container (Optional[list]): The first parameter is a list if you want to instantiate
            an instance with starting values. If provided, a copy of the list is created.
        item_factory(object): The item container that handles item roles and flags along
            with the data.
    
    """

    def __init__(self, container=None, item_factory=ItemContainer):
        super(BaseListModel, self).__init__()
        if container is None:
            container = []
        self._item_factory = item_factory
        self._container = [item_factory(e) for e in container] 


    def columnCount(self, parent=None):
        """Returns 1 because lists do not have multiple columns.

        Note:
            This method overrides the virtual function of it's parent.

        """
        return 1

    def rowCount(self, parent=None):
        """Returns the length of the underlying list.

        Note:
            This method overrides the virtual function of it's parent.

        """
        if parent is None:
            return 0
        return len(self._container)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """Just retuerns the section of the header, lists do not usually have headers.

        Note:
            This method overrides the virtual function of it's parent.

        """
        return unicode(section)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """Sets the data of a role at a specific index of the list.
        If the role is DisplayRole or EditRole, sets the value located
        in the underlying list at the index. Else sets the role of the
        individual item specifically.

        This method is expanded to also accept a new role, you can set item
        flags by passing in the role QtCore.Qt.ItemFlags.

        Args:
            index (QModelIndex):
            role (Optional[ItemRole]):

        Note:
            This method overrides the virtual function of it's parent.

        Raises:
            TypeError: if role is not a instance of ItemDataRole or specifically QtCore.Qt.ItemFlags

        """
        if not index.isValid():
            return None
        row = index.row()
        self._container[row][role] = value
        self.dataChanged.emit(index, index)
        return True

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
        try:
            return self._container[row][role]
        except KeyError as e:
            return None
    
    #todo docs
    def flags(self, index):
        """Returns the QtCore.Qt.ItemFlags of the item at the index.

        You can set item flags using the setData method.
        
        Note:
            This method overrides the virtual function of it's parent.

        """
        if not index.isValid():
            return None
        row, column = index.row(), index.column()
        try:
            return self._container[row][QtCore.Qt.ItemFlags]
        except KeyError as e:
            return None

    def __copy__(self, deep_copy_memo=None):
        """Makes a shallow copy of the list and returns a new model of it.
        
        Keyword Args:
            deep_copy_memo (Optional[dict]): Only to be used by a __deepcopy__
                implimentation. If deep_copy_memo is not None, it should be the 
                memo argument of __deep__ copy. 

        """
        cls = self.__class__
        if deep_copy_memo is None:
            #a bit redundant considerint __init__ copies anyway, but to be safe.
            container = copy.copy(self._container)
        else:
            container = copy.deepcopy(self._container, deep_copy_memo)
        new_instance = cls(self._container)
        return new_instance

    def __deepcopy__(self, memo):
        """Makes a deepcopy of the list and returns a new model of it."""
        return self.__copy__(deep_copy_memo=memo)


class ListModel(MutableSequence, BaseListModel):
    """A python list like implimentation of a QAbstractListModel.
    
    Instances of this class function as both a QAbstractListModel and
    a python list (MutableSequence specifically). This allows you to 
    interact with the object like any other python list through convenient
    methods and index access, but with the benifit of updating all 
    connected views. The connected Qt views can also edit and change the 
    list.
    
    Note:
        ListModel.index_of is the method for MutableSequence.index. 
        ListModel.index is the QAbstractListModel.index method.
        
        This object emits two signals in addition to the signals emited by
            QAbstractListModel.
        ListChanged (Signal(int, object)): A Qt Signal that emits when a value at
            an index in the list changes. Emits the index and previous value changed.
        ListCleared (Signal()): Emited when the list is cleared.

    """
    ListChanged = QtCore.Signal(int, object) 
    ListCleared = QtCore.Signal() 

    
    def _convert_idx(self, idx):
        """To be compatable with Qt objects, ensure the index is a positive number.
        Used for python index operations."""
        #TODO slicing
        if isinstance(idx, slice):
            raise NotImplementedError("No slice setting functionality yet.")
        if idx < 0:
            #idx -1 on a length 10 list is the same as idx 9 (10 + -1)
            idx = len(self) + idx
        return idx

    #MutableSequence Abstract Methods
    def __getitem__(self, idx):
        """Gets the data located the the index or slice in the underlying list.
        
        Note:
            This method is an abstract method required for MutableSequence.
        """
        return self._container.__getitem__(idx).data

    def __setitem__(self, idx, value):
        """Sets the data located the the index or slice in the underlying list.
        
        Note:
            This method is an abstract method required for MutableSequence.
        """
        idx = self._convert_idx(idx)
        index = self.index(idx, 0)
        previous = self._container[idx].data
        self.setData(index, value)
        self.ListChanged.emit(idx, previous)
        return 

    def __delitem__(self, idx):
        """Deletes an item from the underlying list and any associated metadata,
        then updates the model.
        
        Note:
            This method is an abstract method required for MutableSequence.
        """
        idx = self._convert_idx(idx)
        previous = self._container[idx].data
        parent = QtCore.QModelIndex()
        self.beginRemoveRows(parent, idx, idx) 
        ret_value = self._container.__delitem__(idx)
        self.endRemoveRows()
        self.ListChanged.emit(idx, previous)
        return ret_value
    
    def __len__(self, *args):
        """Returns the length of the underlying list.
        
        Note:
            This method is an abstract method required for MutableSequence.
        """
        return self._container.__len__(*args)
    
    def insert(self, idx, value):
        """Inserts data into the underlying list.

        Note:
            This method is an abstract method required for MutableSequence."""
        previous = None
        try:
            previous = self._container[idx].data
        except IndexError:
            pass
        parent = QtCore.QModelIndex()
        self.beginInsertRows(parent, idx, idx)
        ret_value = self._container.insert(idx, self._item_factory(value))
        self.endInsertRows()
        self.ListChanged.emit(idx, previous)
        return ret_value
 
    #Index needs to use QAbstractListModel Index
    def index(self, row, column, parent=QtCore.QModelIndex()):
        """Returns the QModelIndex from the underlying model.
        
        Note:
            This method overrides the virtual function of QAbstractListModel.
            This is not the MutableSequence.index method. That is index_of.
        """
        return QtCore.QAbstractListModel.index(self, row, column, parent=parent)
    
    #QListModel index method overrides Sequence index method
    def index_of(self, item):
        """Calls the python version of list.index.
        Returns the index of the item that matches first."""
        return super(ListModel, self).index(item)
    
    def clear(self):
        """Clears entire model and emits layout changed"""
        self.layoutAboutToBeChanged.emit()
        self._container = self._container[:]
        self.layoutChanged.emit()
        self.ListCleared.emit()

    # Other Python Special Methods
    def __str__(self):
        """Returns the __str__ of the underlying list."""
        return list(self).__str__()
    
    def __repr__(self):
        """The representation of the object, does not include any of the metadata
        such as flags and roles."""
        class_name = self.__class__.__name__
        list_repr = list(self).__repr__()
        factory_name = self._item_factory.__name__
        return "{}({}, item_factory={})".format(class_name, list_repr, factory_name)

    def __eq__(self, *args):
        """Returns whether the underlying list equals another list."""
        return list(self).__eq__(*args)

    def __ne__(self, *args):
        """Returns whether the underlying list is not equal to another list."""
        return list(self).__ne__(*args)