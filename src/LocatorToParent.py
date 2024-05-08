from PySide2.QtCore import Signal
from PySide2.QtGui import QIntValidator, QRegExpValidator 
import maya.cmds as mc
from PySide2.QtWidgets import QCheckBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget, QAbstractItemView

class Locator:
    def __init__(self):
        self.srcMeshes = set()                              #Selected Mesh where the Locator will go to
        self.parentMeshes = set()                           #Selected Mesh(es) where the locator _GRP will be located to               #Roration Values for Locator _GRP
        self.LocatorGrpName = "Locator_GRP"

    def AddSrcMesh(self):
        self.LocatorName = "Locator_" + self.srcMeshes
        selection = mc.ls(sl=True)
        if not selection:
            return False, "No Mesh Selected"
        self.srcMeshes.clear()
        mc.group (self.srcMeshes, self.LocatorName)
        mc.group (self.LocatorName, self.LocatorGrpName)

        if selection > 1:
            return False, "Only select 1 Mesh for Locator to be placed!"
        for selected in selection:
            self.srcMeshes.add(selected)

    def SelectParent(self):
        Parentselection = mc.ls(sl =True)
        if not Parentselection:
            return False, "No Parent(s) selected, please select 1 or more Parent!"
        self.parentMeshes.clear()
        for seleceted in Parentselection:
            self.parentMeshes.add(seleceted)

    def ParentConstraint(self, LocatorGrpName):
        ConstraintToParent = mc.ls(s = True, type = 'transform') [1:]
        for Constraint in ConstraintToParent:
            mc.parentConstraint(Constraint, LocatorGrpName)

    def MatchTransformations(self, LocatorGrpName, Parentselection):
        if LocatorGrpName and Parentselection:
            mc.delete(mc.parentConstraint(LocatorGrpName, Parentselection))
            mc.makeIdentity(LocatorGrpName, a = True, t = True)
        ConstraintToParent = mc.ls(s = True, type = 'transform') [1:]
        for Constraint in ConstraintToParent:
            mc.parentConstraint(Constraint, LocatorGrpName)


    def SetSelectedAsSrcMesh(self):
        selection = mc.ls(sl=True)
        self.srcMeshes.clear() # removes all elements in the set.
        for selected in selection:
            shapes = mc.listRelatives(selected, s=True) # find all shapes of the selected object
            for s in shapes:
                if mc.objectType(s) == "mesh": # the object is a mesh
                    self.srcMeshes.add(selected) # add the mesh to our set.

        mc.setAttr(self.LocatorGrpName + ",".join(self.srcMeshes), type = "string")
            
class LocatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.locatorClass = Locator()
        self.setWindowTitle("Locator Creator")
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.srcMeshList = QListWidget() # create a list to show stuff.
        self.srcMeshList.setSelectionMode(QAbstractItemView.ExtendedSelection) # allow multi-seleciton
        self.srcMeshList.itemSelectionChanged.connect(self.SrcMeshSelectionChanged)
        self.srcMeshList.addItems(self.locatorClass.srcMeshes)
        self.masterLayout.addWidget(self.srcMeshList) # this adds the list created previously to the layout.

        addSrcMeshBtn = QPushButton("Add Source Mesh")
        addSrcMeshBtn.clicked.connect(self.AddSrcMeshBtnClicked)
        self.masterLayout.addWidget(addSrcMeshBtn)

        self.ParentMeshList = QListWidget()
        self.ParentMeshList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ParentMeshList.itemSelectionChanged.connect(self.SrcMeshSelectionChanged)
        self.ParentMeshList.addItem(self.locatorClass.parentMeshes)
        self.masterLayout.addWidget(self.ParentMeshList)

        addParentBtn = QPushButton("Add Parent")
        addParentBtn.clicked.connect(self.AddSrcMeshBtnClicked)
        self.masterLayout.addWidget(addParentBtn)

        MatchTransformationsCB = QCheckBox()
        MatchTransformationsCB.clicked.connect(self.locatorClass.MatchTransformations)
        self.masterLayout.addWidget(MatchTransformationsCB)

        MakeConstraintBtn = QPushButton("Make Parent Constraint")
        MakeConstraintBtn.clicked.connect(self.locatorClass.ParentConstraint)
        self.masterLayout.addWidget(MakeConstraintBtn)




        
    def SrcMeshSelectionChanged(self):
        mc.select(cl=True) # this deselect everything.
        for item in self.srcMeshList.selectedItems():
            mc.select(item.text(), add = True)

    def AddSrcMeshBtnClicked(self):
        self.locatorClass.SetSelectedAsSrcMesh() # asks ghost to populate it's srcMeshes with the current selection
        self.srcMeshList.clear() # this clears our list widget
        self.srcMeshList.addItems(self.locatorClass.srcMeshes) # this add the srcMeshes collected eariler to the list widget
        



locatorWidget = LocatorWidget()
locatorWidget.show()