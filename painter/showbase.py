"""
"""

from panda3d import core as p3d
from direct.showbase.ShowBase import ShowBase
from painter import runtime

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class PainterShowBase(ShowBase):
    """
    """

    def __init__(self, fStartDirect=True, windowType=None):

        super().__init__(fStartDirect=fStartDirect, windowType=windowType)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
