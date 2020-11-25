"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from panda3d import core as p3d
from painter import runtime, showbase, vfs
from functools import partial

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QItemDetails(QtWidgets.QWidget):
    """
    """

    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._regionBtns = {}
        self._initializeGui()

    def _initializeGui(self) -> None:
        """
        """

        grid = QtWidgets.QGridLayout()

        infoBox = QtWidgets.QGroupBox('Item Information')
        infoBoxLayout = QtWidgets.QVBoxLayout()
        infoBoxLayout.setSpacing(0)

        self.itemName = QtWidgets.QLineEdit()
        self.itemName.setText('Item')
        infoBoxLayout.addWidget(self.itemName)

        self.itemTooltip = QtWidgets.QLineEdit()
        self.itemTooltip.setText('Example Tooltip')
        infoBoxLayout.addWidget(self.itemTooltip)

        self.itemSelect = QtWidgets.QComboBox()
        self.itemSelect.addItems(runtime.library.items)
        self.itemSelect.currentIndexChanged.connect(self._handleItemTypeChange)
        infoBoxLayout.addWidget(self.itemSelect)

        btnBox = QtWidgets.QGroupBox('Color Regions')
        btnBoxLayout = QtWidgets.QVBoxLayout()
        channels = runtime.editor_state.get_channel_list()
        index = 0
        for channel in channels:
            btn = self._createRegionButton(index, channel, btnBoxLayout)
            self._regionBtns[channel] = btn
            index += 1

        infoBox.setLayout(infoBoxLayout)
        btnBox.setLayout(btnBoxLayout)

        grid.addWidget(infoBox)
        grid.addWidget(btnBox)
        self.setLayout(grid)
        self._updateRegions()

    def _createRegionButton(self, index: int, channel: str, layout: object) -> QtWidgets.QPushButton:
        """
        """

        index += 1
        button = QtWidgets.QPushButton('Color Region #%s' % index)
        button.setToolTip('Opens the color dialog to recolor region #%s' % index)
        button.clicked.connect(partial(self._handleRegionColorPress, channel))

        layout.addWidget(button)
        return button

    def _handleRegionColorPress(self, channel: int) -> None:
        """
        """

        color = QtWidgets.QColorDialog.getColor(
            initial=runtime.editor_state.get_channel(channel))
        if color.isValid():
            runtime.editor_state.set_channel(channel, color)

    def _handleItemTypeChange(self, index: int) -> None:
        """
        """
    
        item_type = runtime.library.items[index]
        runtime.editor_state.item_type = item_type
        self._updateRegions()

    def _updateRegions(self) -> None:
        """
        """

        item_type = runtime.editor_state.item_type
        item_data = runtime.library.itemData[item_type]
        
        regions = item_data['Regions']
        for key, val in regions.items():
            channel = key.capitalize()
            self._regionBtns[channel].setEnabled(int(val))

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

        # Create our display quad
        cardMaker = p3d.CardMaker("ItemCard")
        cardMaker.set_frame(-0.8, 0.8, -0.8, 0.8)
        self.itemCard = self.base.aspect2d.attach_new_node(cardMaker.generate())
        runtime.itemCard = self.itemCard

        shader = p3d.Shader.load(p3d.Shader.SL_GLSL,
            vertex='shader/item.vert.glsl',
            fragment='shader/item.frag.glsl')
        self.itemCard.set_shader(shader)

        self.itemCard.set_shader_input('pnt_RedChannel',        p3d.Vec3(0, 0, 0))
        self.itemCard.set_shader_input('pnt_GreenChannel',      p3d.Vec3(0, 0, 0))
        self.itemCard.set_shader_input('pnt_BlueChannel',       p3d.Vec3(0, 0, 0))
        self.itemCard.set_shader_input('pnt_CyanChannel',       p3d.Vec3(0, 0, 0))
        self.itemCard.set_shader_input('pnt_MagentaChannel',    p3d.Vec3(0, 0, 0))
        self.itemCard.set_shader_input('pnt_YellowChannel',     p3d.Vec3(0, 0, 0))
        self.itemCard.set_shader_input('pnt_BlackoutChannel',   p3d.Vec3(1, 1, 1))

        # Configure our VFS and populate our library
        vfs.switch_file_functions_to_vfs()
        vfs.switch_io_functions_to_vfs()
        runtime.library.pullConfiguration()

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
