"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from panda3d import core as p3d

from painter import widgets, runtime, item
from painter import __version__

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class EditorState(object):
    """
    """

    def __init__(self):
        runtime.editor_state = self

        self._name = 'Example Item'
        self._tooltip = 'Example Tooltip'
        self._item_type = None
        self._dirty = False

        self._channels = {
            'Red':      QtGui.QColor(0, 0, 0),
            'Green':    QtGui.QColor(0, 0, 0),
            'Blue':     QtGui.QColor(0, 0, 0),
            'Cyan':     QtGui.QColor(0, 0, 0),
            'Magenta':  QtGui.QColor(0, 0, 0),
            'Yellow':   QtGui.QColor(0, 0, 0),
            'Blackout': QtGui.QColor(255, 255, 255)
        }

    ##########################
    ###        Info        ###
    ##########################

    def name(self) -> str:
        """
        """

        return self._name

    def name(self, name: str) -> None:
        """
        """

        self._dirty = True
        self._name = name

    ##########################
    ###        Type        ###
    ##########################

    @property
    def item_type(self) -> str:
        """
        """

        return self._item_type

    @item_type.setter
    def item_type(self, item_type: str) -> None:
        """
        """

        self._item_type = item_type
        item_data = runtime.library.itemData[item_type]
        images = item_data['Images']

        detail = runtime.loader.load_texture(images['detail'])
        mask = runtime.loader.load_texture(images['mask'])
        mask_stage = p3d.TextureStage('mask')

        runtime.itemCard.set_texture_off()
        runtime.itemCard.set_texture(detail)
        runtime.itemCard.set_texture(mask_stage, mask)
        runtime.itemCard.set_transparency(True)

    ##########################
    ###      Channels      ###
    ##########################

    def get_channel_list(self) -> list:
        """
        """

        return list(self._channels.keys())

    def get_channel(self, key: str) -> object:
        """
        """

        return self._channels.get(key, None)

    def set_channel(self, key: str, color: object) -> None:
        """
        """

        self._dirty = True
        shader_input = (color.red()/255, color.green()/255, color.blue()/255)
        self._channels[key] = color
        shader_input_name = 'pnt_%sChannel' % key
        runtime.itemCard.set_shader_input(shader_input_name, shader_input)

    ##########################
    ### File Serialization ###
    ##########################

    def to_file(self, filename: str) -> None:
        """
        """

    @classmethod
    def from_file(cls, filename: str) -> object:
        """
        """

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

        self._library = item.ItemLibrary('config')
        self._state = EditorState()

    def _initializeGui(self) -> None:
        """
        """

        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout.setSpacing(2)

        horizontalLayout1 = QtWidgets.QHBoxLayout()
        horizontalLayout2 = QtWidgets.QHBoxLayout()

        self.viewport = widgets.QViewportWidget()
        self.colorpicker = widgets.QItemDetails()

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
