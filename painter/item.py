"""
"""

from panda3d import core as p3d
from painter import runtime, vfs

import configparser

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class ItemData(object):
    """
    """

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

    def pullConfiguration(self) -> None:
        """
        """

        itemFiles = vfs.get_matching_files(self._itemPath, '*.ini')
        for itemFile in itemFiles:
            self._loadItemFile(itemFile)
        runtime.editor_state.item_type = self._items[0]

    def _loadItemFile(self, filename: str) -> None:
        """
        """

        parser = configparser.RawConfigParser()
        parser.read(filename)

        item_key = parser['Info']['name']
        self._items.append(item_key)

        data = {}
        for section in parser.sections():
            data[section] = {}
            for key, val in parser.items(section):
                data[section][key] = val
        self._itemData[item_key] = data
