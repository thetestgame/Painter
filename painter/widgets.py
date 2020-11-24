"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from panda3d import core as p3d
from painter import runtime, showbase

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
        
        return QtCore.QSize(400,300)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
