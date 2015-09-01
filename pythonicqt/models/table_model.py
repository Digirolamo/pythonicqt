"""This module contains the class and data structures that make
the TableModel class.
"""

import six
from collections import MutableSequence
from pythonicqt.Qt import QtCore
from six.moves import xrange
from pythonicqt.baseclasses import QtMetaStitch
from pythonicqt.models.modelitems import ItemContainer


@six.add_metaclass(QtMetaStitch)
class BaseTableModel(QtCore.QAbstractTableModel):
    """"A working implimentation of QAbstractTableModel."""

    def __init__(self, *args, **kwargs):
        super(BaseTableModel, self).__init__(*args, **kwargs)
        if not self._container:
            self.column_count = 0
        else:
            self.column_count = len(self._container[0])
        #Containers for the header data
        self._header_data = {
                QtCore.Qt.Horizontal: [item_factory(num) for num in xrange(self.column_count)],
                QtCore.Qt.Vertical: [item_factory(num) for num in xrange(self._container)],
                }

    def columnCount(self, parent=None):
        """Returns the the column count.
        Note:
            This method overrides the virtual function of it's parent.
        """
        return self.column_count

    def setHeaderData(self, section, orientation, value, role=QtCore.Qt.QEditRole):
        """Sets the header data.

        Note:
            This method overrides the virtual function of it's parent.
        """
        self._header_data[orientation][section][role] = value

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """Returns the header data of the item, default is the column or list number.

        Note:
            This method overrides the virtual function of it's parent.
        """
        return self._header_data[orientation][section][role]

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
        if not isinstance(role, QtCore.Qt.ItemDataRole) and role is not QtCore.Qt.ItemFlags:
            raise TypeError("role parameter must be a instance of QtCore.Qt.ItemDataRole or QtCore.Qt.ItemFlags "
                            "not {}".format(type(role)))
        if not index.isValid():
            return None
        row, column = index.row(), index.column()
        self._container[row][role] = value
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