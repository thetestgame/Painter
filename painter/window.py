"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from painter import widgets

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QEditorWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(0, 0, 800, 600)

        self.viewport = widgets.QViewportWidget()
        self.setCentralWidget(self.viewport)

    def show(self) -> None:
        """
        """
    
        super().show()
        self.viewport.forceResize()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
