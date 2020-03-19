import MaxPlus
import pymxs
from PySide2 import QtWidgets, QtCore, QtGui
RT = pymxs.runtime
class AniSet():
    def __init__(self, name, startFrame, endFrame):
        self.name = name
        self.start_frame = startFrame
        self.end_frame = endFrame
class FullAniSetView(QtWidgets.QDialog):
    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        pass

