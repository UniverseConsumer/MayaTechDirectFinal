from PySide2.QtCore import Signal
from PySide2.QtGui import QIntValidator, QRegExpValidator 
import maya.cmds as mc
from PySide2.QtWidgets import QCheckBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget, QAbstractItemView

class Locator:
    def __init__(self):
        self.srcMeshes = set()                              #Selected Mesh where the Locator will go to
        self.parentMeshes = set()                           #Selected Mesh(es) where the locator _GRP will be located to
        self.translationsforLocator = [0,0,0]               #Translation Coordinates for Locator _GRP
        self.rotationsforLocator = [0,0,0]                  #Roration Values for Locator _GRP

    def SelectedSrcMesh(self):
        selection = mc.ls(sl=True)
        if not selection:
            return False, "No Mesh Selected"
        self.srcMeshes.clear()
        
        if selection > 1:
            return False, "Only select 1 Mesh for Locator placed!"
        for selected in selection:
            self.srcMeshes.add(selected)

    def SelectParent(self):
        selection = mc.ls(sl =True)
        if not selection:
            return False, "No Parent(s) selected, please select 1 or more Parent!"
        self.parentMeshes.clear()
        for seleceted in selection:
            self.parentMeshes.add(seleceted)
    
    def MakeGRP(Self):
        
        


class LocatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.locator = Locator()
        self.setWindowTitle("Locator Creator by Nathan Garcia")
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

locatorWidget = LocatorWidget()
locatorWidget.show()