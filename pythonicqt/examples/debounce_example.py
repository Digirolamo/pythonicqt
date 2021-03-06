"""debounce example"""
from pythonicqt.Qt import QtCore, QtGui
from pythonicqt.examples import ExampleBase
from pythonicqt import debounce

class ExampleDebounce(ExampleBase):
    """This Widget demonstrates the debounce functionality.
    You can manually change the debounce code in the file
    to play with different debounce arguments."""
    title="Debounce"

    def __init__(self, *args, **kwargs):
        super(ExampleDebounce, self).__init__(*args, **kwargs)
        self._layout = QtGui.QVBoxLayout(self)
        self.description_label = QtGui.QLabel(
            "Quickly change spin box values and watch them update.")
        self._layout.addWidget(self.description_label)
        
        self.debounce_checkbox = QtGui.QCheckBox("use debounce.", checked=True)
        self._layout.addWidget(self.debounce_checkbox)
        
        self.spin_box = QtGui.QSpinBox()
        self.spin_box.setMaximum(100)
        self._layout.addWidget(self.spin_box)
        
        self.value_template = "Last updated value is {}."
        self.last_value_label = QtGui.QLabel(self.value_template.format(0))
        self._layout.addWidget(self.last_value_label)
        
        self.spin_box.valueChanged.connect(self.spin_box_changed)
    
    #This method is called every time the spin box changes.
    #The method redirects the call based on the checkbox state.
    def spin_box_changed(self, new_value):
        update_method = self.update_description
        if self.debounce_checkbox.isChecked():
            update_method = self.update_description_debounced
        update_method(new_value)
        
    def update_description(self, value):
        new_description = self.value_template.format(value)
        self.last_value_label.setText(new_description)
        
    #You can change the debounce arguments to see the effects. 
    @debounce(msecs=200)
    def update_description_debounced(self, value):
        """Changes the label to reflect the value of the spinbox."""
        self.update_description(value)

if __name__ == "__main__":
    ExampleDebounce.run_example()
