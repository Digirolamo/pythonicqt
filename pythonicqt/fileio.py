"""File and IO related classes and functions."""
from contextlib import closing
from pythonicqt.Qt import QtCore, QtGui, QtUiTools


class File(QtCore.QFile):
    """File adds convenience abilities to QFiles open/close behavior..
    Adds python mode support to opening modes."""
    open_mode_dict = {
        'r' :QtCore.QIODevice.ReadOnly,
        'w' :QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Truncate,
        'a' :QtCore.QIODevice.Append,

        'r+' :QtCore.QIODevice.ReadWrite,
        'w+' :QtCore.QIODevice.ReadWrite | QtCore.QIODevice.Truncate,
        'a+' :QtCore.QIODevice.ReadWrite | QtCore.QIODevice.Append,
        }

    def open(self, mode='r'):
        """Adds pythons file open modes (can still use QIODevice.OpenModes).
       Adds a closing context manager to the open method. 
       Returns closing(self)"""
        mode = self.convert_file_mode(mode)
        super(File, self).open(mode)
        return closing(self)

    @staticmethod
    def convert_file_mode(mode):
        """Converts an open mode to a QIODevice.OpenMode. Accepts other OpenModes
        or pythons file open modes ('r', 'w', 'r+', ect.)"""
        if isinstance(mode, QtCore.QIODevice.OpenMode):
            return mode
        while mode[-1] in ['b', 'U']:
            mode = mode[:-1]
        return File.open_mode_dict[mode]


def q_open(file_path, mode='r'):
    """Convenience function for "with x" block.
    with q_open(file_path) as f:
    is Equivlent to writing.
    with File(file_path).open() as f:"""
    q_file = File(file_path)
    return q_file.open(mode)


def load_ui_file(file_path, parent=None):
    """Takes in a filepath and loads and returns the output."""
    ui_loader = QtUiTools.QUiLoader()
    with q_open(file_path) as ui_file:
        output = ui_loader.load(ui_file, parent)
    return output