"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from panda3d import core as p3d

from painter import widgets, runtime, item
from painter import __version__

import os
import configparser

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

    @property
    def name(self) -> str:
        """
        """

        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        """

        self._dirty = True
        self._name = name

    @property
    def tooltip(self) -> str:
        """
        """

        return self._tooltip

    @tooltip.setter
    def tooltip(self, tooltip: str) -> None:
        """
        """

        self._dirty = True
        self._tooltip = tooltip

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

    def set_channel_hex(self, key: str, hex: str) -> None:
        """
        """

        self.set_channel(key, QtGui.QColor(hex))

    ##########################
    ###  State Management  ###
    ##########################

    def is_dirty(self) -> bool:
        """
        """

        return self._dirty

    def clear(self) -> None:
        """
        """

        self._name = 'Example Item'
        self._tooltip = 'Example Tooltip'
        self._dirty = True

        self.set_channel('Red',  QtGui.QColor(0, 0, 0))
        self.set_channel('Green',  QtGui.QColor(0, 0, 0))
        self.set_channel('Blue',  QtGui.QColor(0, 0, 0))
        self.set_channel('Cyan',  QtGui.QColor(0, 0, 0))
        self.set_channel('Magenta',  QtGui.QColor(0, 0, 0))
        self.set_channel('Yellow',  QtGui.QColor(0, 0, 0))
        self.set_channel('Blackout',  QtGui.QColor(255, 255, 255))

        runtime.messenger.send('STATE_CHANGED')

    ##########################
    ### File Serialization ###
    ##########################

    def toFile(self, filename: str) -> None:
        """
        """

        self._dirty = False

        config = configparser.ConfigParser()
        config['Information'] = {}
        config['Information']['Name'] = self._name
        config['Information']['Tooltip'] = self._tooltip
        config['Information']['Type'] = self._item_type
        config['Colors'] = {}
        for channel in self._channels:
            config['Colors'][channel] = self._channels[channel].name()

        with native_open(filename, 'w') as f:
            config.write(f)

    def fromFile(self, filename: str) -> object:
        """
        """

        config = configparser.SafeConfigParser()
        config.read(filename)

        self.name = config['Information']['Name']
        self.tooltip = config['Information']['Tooltip']
        self.item_type = config['Information']['Type']

        for channel in config['Colors']:
            self.set_channel_hex(channel.capitalize(), config['Colors'][channel])

        self._dirty = False
        runtime.messenger.send('STATE_CHANGED')

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
        self.editor_state = EditorState()

    def _initializeGui(self) -> None:
        """
        """

        horizontalLayout = QtWidgets.QHBoxLayout()

        self.viewport = widgets.QViewportWidget()
        self.colorpicker = widgets.QItemDetails()

        horizontalLayout.addWidget(self.viewport)
        horizontalLayout.addWidget(self.colorpicker)

        self.setLayout(horizontalLayout)

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
        self._activeFile = None

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

        self._activeFile = None
        runtime.editor_state.clear()

    def _openFile(self) -> None:
        """
        """

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open  Item File', '', 'Item Ini (*.ini)')
        runtime.editor_state.fromFile(filename)

    def _saveFile(self) -> None:
        """
        """

        self._saveEditorState(True)

    def _saveFileAs(self) -> None:
        """
        """

        self._saveEditorState()

    def _saveEditorState(self, existing: bool = False) -> None:
        """
        """

        filename = None
        if existing and self._activeFile != None:
            filename = self._activeFile
        else:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Item File', '', 'Item Ini (*.ini)')

        if filename == None:
            return

        self._activeFile = filename
        runtime.editor_state.toFile(filename)

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
