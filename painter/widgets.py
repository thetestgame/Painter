"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from panda3d import core as p3d
from painter import runtime, showbase

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QRegionColorPicker(QtWidgets.QWidget):
    """
    """

    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._regionBtns = {}
        self._initializeViewport()

    def _initializeViewport(self) -> None:
        """
        """

        grid = QtWidgets.QGridLayout()

        infoBox = QtWidgets.QGroupBox('Item Information')
        infoBoxLayout = QtWidgets.QVBoxLayout()

        btnBox = QtWidgets.QGroupBox('Color Regions')
        btnBoxLayout = QtWidgets.QVBoxLayout()
        for index in range(6):
            btn = self._createRegionButton(index, btnBoxLayout)
            self._regionBtns[index] = btn

        infoBox.setLayout(infoBoxLayout)
        btnBox.setLayout(btnBoxLayout)

        grid.addWidget(infoBox)
        grid.addWidget(btnBox)
        self.setLayout(grid)

    def _createRegionButton(self, index: int, layout: object) -> QtWidgets.QPushButton:
        """
        """

        index += 1
        button = QtWidgets.QPushButton('Color Region #%s' % index)
        button.setToolTip('Opens the color dialog to recolor region #%s' % index)
        button.clicked.connect(self._handleRegionColorPress)

        layout.addWidget(button)
        return button

    def _handleRegionColorPress(self) -> None:
        """
        """

        color = QtWidgets.QColorDialog.getColor()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QViewportWidget(QtWidgets.QWidget):
    """
    """

    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initializeViewport()
        runtime.viewport = self

    def _initializeViewport(self) -> None:
        """
        """

        # Initialize our ShowBase instance
        wp = p3d.WindowProperties.getDefault()
        wp.set_size(self.width(), self.height())
        wp.set_origin(0, 0)
        wp.set_parent_window(int(self.winId()))
        wp.set_undecorated(True)

        self.base = showbase.PainterShowBase(windowType='none')
        self.base.windowType = 'onscreen'
        self.base.openDefaultWindow(props=wp)
        self.base.set_background_color(0, 0, 0, 1)

        # Setup our task manager step timer
        self._pandaTimer = QtCore.QTimer(self)
        self._pandaTimer.timeout.connect(base.task_mgr.step)
        self._pandaTimer.start(0)

    def forceResize(self) -> None:
        """
        """

        wp = p3d.WindowProperties()
        wp.set_origin(0, 0)
        wp.set_size(self.width(), self.height())
        self.base.win.requestProperties(wp)

    def resizeEvent(self, evt: object) -> None:
        """
        """
        
        size = evt.size()
        wp = p3d.WindowProperties()
        wp.setOrigin(0, 0)
        wp.setSize(size.width(), size.height())
        self.base.win.requestProperties(wp)

    def minimumSizeHint(self) -> QtCore.QSize:
        """
        """
        
        return QtCore.QSize(600,300)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
