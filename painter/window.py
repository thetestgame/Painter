"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from painter import widgets, runtime, library
from painter import __version__

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QEditor(QtWidgets.QWidget):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        runtime.editor = self

        self._initalizeManagers()
        self._initializeGui()

    def _initalizeManagers(self) -> None:
        """
        """

        self._library = library.ItemLibrary('items')

    def _initializeGui(self) -> None:
        """
        """

        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout.setSpacing(2)

        horizontalLayout1 = QtWidgets.QHBoxLayout()
        horizontalLayout2 = QtWidgets.QHBoxLayout()

        self.viewport = widgets.QViewportWidget()
        self.colorpicker = widgets.QRegionColorPicker()

        horizontalLayout1.addWidget(self.viewport)
        horizontalLayout1.addWidget(self.colorpicker)

        verticalLayout.addLayout(horizontalLayout1)
        verticalLayout.addLayout(horizontalLayout2)

        self.setLayout(verticalLayout)

    def show(self) -> None:
        """
        """
    
        super().show()
        self.viewport.forceResize()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QEditorWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        runtime.window = self

        self._initializeViewport()

    def _initializeViewport(self) -> None:
        """
        """

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self._createAction('&New', status='Creates a new Painter project', callback=self._newFile))
        fileMenu.addAction(self._createAction('&Open', status='Opens a Painter project', callback=self._openFile))
        fileMenu.addAction(self._createAction('&Save', status='Saves the current Painter project', callback=self._saveFile))
        fileMenu.addAction(self._createAction('&Save As', status='Saves the current Painter project as a specific name', callback=self._saveFileAs))

        fileMenu.addSeparator()
        fileMenu.addAction(self._createAction('&Exit', status='Closes Painter', callback=QtWidgets.qApp.quit))
        menubar.addAction(self._createAction('&About', status='Opens the about dialog', callback=self._openAbout))

        self.setGeometry(0, 0, 800, 600)
        self.setFixedSize(800, 600)
        self.setCentralWidget(QEditor())

    def _createAction(self, text: str, status: str, callback: object = None) -> None:
        """
        """

        action = QtWidgets.QAction(text, self)
        action.setStatusTip(status)
        
        if callback != None:
            assert callable(callback)
            action.triggered.connect(callback)

        return action

    def _newFile(self) -> None:
        """
        """

    def _openFile(self) -> None:
        """
        """

    def _saveFile(self) -> None:
        """
        """

    def _saveFileAs(self) -> None:
        """
        """

    def _openAbout(self) -> None:
        """
        """

        QtWidgets.QMessageBox.about(self, 
            'About',  
            """
            6 Channel Item Painting Utility.
            Created By: Jordan Maxwell (thetestgame)
            Version: %s
            """ % __version__)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
