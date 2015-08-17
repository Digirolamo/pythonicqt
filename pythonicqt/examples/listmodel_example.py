"""An example of the ListModel."""
from PySide import QtCore, QtGui
from pythonicqt import ListModel
from pythonicqt.examples import ExampleBase

class ExampleListModel(ExampleBase):
    """This Widget demonstrates the ListModel functionality.
    You can interactwith a model that behaves like a
    Python list (self.list_model), at the same time the model propagates changes
    correcly."""
    title="ListModel"

    def __init__(self, *args, **kwargs):
        super(ExampleListModel, self).__init__(*args, **kwargs)
        self.list_model = ListModel([1, 'two', u'three'])
        #The Views
        self._layout = QtGui.QVBoxLayout(self)
        self.combo_one = QtGui.QComboBox()
        self._layout.addWidget(self.combo_one)
        self.combo_two = QtGui.QComboBox()
        self._layout.addWidget(self.combo_two)
        self.label = QtGui.QLabel("You can edit the items below.")
        self._layout.addWidget(self.label)
        self.list_view = QtGui.QListView()
        self._layout.addWidget(self.list_view)
        #Connect Model to Views
        self.combo_one.setModel(self.list_model)
        self.combo_two.setModel(self.list_model)
        self.list_view.setModel(self.list_model)

        #Example interaction
        self.list_model.append("Now Last")
        self.list_model.insert(0, 'Now First')


if __name__ == "__main__":
    ExampleListModel.run_example()