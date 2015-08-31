"""This file creates the example selector allowing the user to view all of the examples.
It is intended to run as the main entry point of examples.

You can run this file by writing "python -m pythonicqt.examples"
"""
import os
import sys
from pythonicqt.Qt import QtGui
from pythonicqt.examples.example_selector import AllExamples

def run_examples():
    """Creates a QApplication and opens the example selector."""
    app = QtGui.QApplication(sys.argv)
    dir_path, file_name =  os.path.split(os.path.abspath(__file__))
    ui_path = os.path.join(dir_path, "examples_ui.ui")
    all_examples = AllExamples(ui_path)
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_examples()
