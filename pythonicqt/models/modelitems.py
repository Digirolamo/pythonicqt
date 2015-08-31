"""This module should contain all of the types of containers that
hold the flags and data roles of items in models.

"""

from pythonicqt.Qt import QtCore


class ItemContainer(dict):
    """A dictionary used to hold a QAbstractModel item's data and flags.

    In Qt models, every item in a model can have specific data and flags.
    Instances of this class contains flags and roles of a specific item.
    If a specific item does not have a set role, tries to return a default role
    if the class variable default_data has any. 
    
    EditRole usualy returns the actual data, DisplayRole returns a unicode version
    of the data.
    
    Attributes:
        default_data (ItemFlag): The default flags and  roles that all of the items return.
            Change an instance variable of the same name, or subclass this class
            and redefine this attribute if you want to use different flags.
    """
    default_data = {
        QtCore.Qt.ItemFlags: 
            (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | 
             QtCore.Qt.ItemIsEditable)
        }

    def __init__(self, item_data, role=QtCore.Qt.EditRole):
        self[role] = item_data

    @property
    def data(self):
        """Convenient property that returns the default data.

            Rather 
        """
        return self[QtCore.Qt.EditRole]

    def __getitem__(self, key):
        """Returns the data or flags of this dictionary item.
       
        Returns:
            ItemData or ItemRole: If the key is in this instances dictionary, returns
                that value. Otherwise, looks if the key is in the default_data dictionary
                and returns that value. Else raises KeyError.
        """
        if key in self:
            return super(ItemContainer, self).__getitem__(key)
        elif key == QtCore.Qt.DisplayRole:
            return unicode(self.data)
        else:
            #This raises a KeyError if no default exists.
            return self.default_data[key]

    def __setitem__(self, key, value):
        """Sets the data or flags of the item.
        
        Raises:
            TypeError: if role is not a instance of ItemDataRole or specifically QtCore.Qt.ItemFlags
        """
        super(ItemContainer, self).__setitem__(key, value)