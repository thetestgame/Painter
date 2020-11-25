"""
"""

from panda3d import core as p3d
from painter import runtime

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ItemLibrary(object):
    """
    """

    def __init__(self, item_path: str):
        runtime.library = self
        self._itemPath = item_path

        self._items = []
        self._itemData = {}

    @property
    def items(self) -> list:
        """
        """

        return self._items

    @property
    def itemData(self) -> dict:
        """
        """

        return self._itemData

    def pullConfiguration(self, ) -> None:
        """
        """

        self._items = ['Ring01', 'Ring02', 'Ring03'] * 50