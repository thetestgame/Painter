"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from panda3d import core as p3d

from painter import editor, __version__
from painter import vfs, runtime

import os
import sys
import ctypes
import easygui

try:
    import qdarkstyle
    has_dark = True
except ImportError:
    has_dark = False

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class PainterApplication(QtWidgets.QApplication):
    """
    Primary QApplication instance for the Painter item editor
    """

    def __init__(self, *args, dev: bool = False, **kwargs):
        super().__init__(*args, **kwargs)

        self._initalizeApplication(dev)

    def _initalizeApplication(self, dev: bool) -> None:
        """
        Performs application intialization steps
        """

        # Configure our PyQt5 environment
        if has_dark:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setApplicationDisplayName('Painter')
        self.setApplicationName('Painter')
        self.setApplicationVersion(__version__)
        runtime.app = self

        # Mount our application virtual file system
        if dev:
            vfs.vfs_mount_subdirectories('.', 'assets')
            vfs.vfs_mount_subdirectories('.', 'items')
        else:
            self._mountMultifile('assets.mf')
            self._mountMultifile('items.mf')

        # Initialize Panda3D environment variables
        p3d.load_prc_file('config/painter.prc')

        # Initialize our editor window
        self._window = editor.QEditorWindow()
        self._window.show()

    def _mountMultifile(self, path: str) -> None:
        """
        Mounts the requested multifile path
        """

        success = vfs.vfs_mount_multifile('.', path)
        if not success:
            self.showErrorDialog(message='Failed to mount %s' % path)
            sys.exit(2)

    def showErrorDialog(self, message: str, title: str = 'Critical Error') -> None:
        """
        Displays a error dialog box to the user
        """

        if os.name == 'nt':
            ctypes.windll.user32.MessageBoxW(0, message, title, 0)
        else:
            easygui.msgbox(message, title=title)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
