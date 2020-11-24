"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from wecs.panda3d import core

from painter import window

try:
    import qdarkstyle
    has_dark = True
except ImportError:
    has_dark = False

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class PainterApplication(QtWidgets.QApplication):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if has_dark:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setApplicationDisplayName('Painter')
        self.setApplicationName('Painter')
        self.setApplicationVersion('1.0.0')

        self._window = window.QEditorWindow()
        self._window.show()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
