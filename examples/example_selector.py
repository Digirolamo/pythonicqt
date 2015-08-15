"""A window where you can load all examples."""
import os, sys, types, traceback
from PySide import QtGui
from pythonicqt.fileio import load_ui_file
from examplebase import MetaExample
import debounce

def make_module(name, source):
    """The code in tests is imported as a fake temporary module."""
    module = types.ModuleType( name, source )
    module.__file__ = name + '.pyc'
    byte_code = compile(source, name, 'exec')
    exec byte_code in module.__dict__
    return module

class AllExamples(object):
    """Controller for all example selection."""
    def __init__(self, ui_path):
        self.current_widget = None
        self.example_selector = load_ui_file(ui_path)
        print MetaExample.all_examples
        for module_name, example_class in MetaExample.all_examples.iteritems():
            item = QtGui.QListWidgetItem(example_class.title)
            item.example_module = module_name
            self.example_selector.example_list.addItem(item)
        self.example_selector.example_list.currentItemChanged.connect(self.set_example_selected)
        self.example_selector.run_btn.clicked.connect(self.run_code)
        self.example_selector.reload_btn.clicked.connect(self.reload_selected)

        #Set the initial example to the first item
        first_item = self.example_selector.example_list.item(0)
        self.example_selector.example_list.setCurrentItem(first_item)
        self.example_selector.show()

    def set_example_selected(self, item, previous):
        """Sets an example based on the items in the QListWidget."""
        if not hasattr(item, 'example_module'):
            self.example_selector.code_editor.clear()
            self.example_selector.file_name_line_edit.setText("No Example Selected")
        else:
            example_name = item.text()
            module_name = item.example_module
            path = os.path.abspath(sys.modules[module_name].__file__)
            # get the .py not the .pyc
            if path[-1] == 'c':
                path = path[:-1]
            description = "{}: {}".format(example_name, path)
            self.example_selector.file_name_line_edit.setText(description)
            full_text = "".join(open(path).readlines())
            self.example_selector.code_editor.setPlainText(full_text)

    def reload_selected(self):
        """Reloads the currently selected example code. Effectively undoes any changes."""
        item = self.example_selector.example_list.currentItem()
        self.set_example_selected(item, None)

    def run_code(self):
        """Runs the code in the editor and loads the module as that code."""
        if self.current_widget is not None:
            self.current_widget.deleteLater()
        print len(MetaExample.all_examples)
        code_text = self.example_selector.code_editor.toPlainText()
        item = self.example_selector.example_list.currentItem()
        try:
            module = make_module(item.example_module, code_text)
            example_widget = MetaExample.all_examples[item.example_module]
            self.current_widget = example_widget()
            self.current_widget.show()
        except Exception as e:
            #So the user sees errors they create.
            QtGui.QMessageBox.warning(self.example_selector, "Error", traceback.format_exc())
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dir_path, file_name =  os.path.split(os.path.abspath(__file__))
    ui_path = os.path.join(dir_path, "examples_ui.ui")
    all_examples = AllExamples(ui_path)
    sys.exit(app.exec_())
