import maya.cmds as mc
from PySide2.QtWidgets import QCheckBox, QListWidget, QPushButton, QVBoxLayout, QWidget, QAbstractItemView

class Locator:
    def __init__(self):
        self.srcMeshes = set()                              #Selected Mesh where the Locator will go to
        self.parentMeshes = set()                           #Selected Mesh(es) where the locator _GRP will be located to
        self.LocatorGrpName = "Locator_GRP"                 #Defines the LocatorGRPName

    def AddSrcMesh(self):
        self.LocatorName = "Locator_" + self.srcMeshes      #Defines the Locator Name
        selection = mc.ls(sl=True)                          #Makes sures thetere is a selection
        if not selection:
            return False, "No Mesh Selected"                #If there is no selection
        self.srcMeshes.clear()                              #Clear the selection
        mc.group (self.srcMeshes, self.LocatorName)         #Group the Selected Mesh to the Locator
        mc.group (self.LocatorName, self.LocatorGrpName)    #Group the Locator to the Locator_GRP

        if selection > 1:                                   #Only 1 Selection for the Source Mesh can be made
            return False, "Only select 1 Mesh for Locator to be placed!"
        for selected in selection: 
            self.srcMeshes.add(selected)                    #Add the Selected Mesh to the List

    def SelectParent(self):                                 
        Parentselection = mc.ls(sl =True)                   #Makes sure that an OBJ can be selected
        if not Parentselection:
            return False, "No Parent(s) selected, please select 1 or more Parent!"
        self.parentMeshes.clear()                           #Clear the Selection List
        for seleceted in Parentselection:
            self.parentMeshes.add(seleceted)                #Add the parent to the Selection List

    def ParentConstraint(self, LocatorGrpName):
        ConstraintToParent = mc.ls(s = True, type = 'transform') [1:]   #Selects the Locator_GRP and The Parent in the List
        for Constraint in ConstraintToParent:
            mc.parentConstraint(Constraint, LocatorGrpName)             #Make the Constraint from the Locator to the Parent

    def MatchTransformations(self, LocatorGrpName, Parentselection):    
        if LocatorGrpName and Parentselection:
            mc.delete(mc.parentConstraint(LocatorGrpName, Parentselection)) #Deletes any Parent Contraint
            mc.makeIdentity(LocatorGrpName, a = True, t = True)             #Matches the Transformations to the Parent
        ConstraintToParent = mc.ls(s = True, type = 'transform') [1:]
        for Constraint in ConstraintToParent:                               
            mc.parentConstraint(Constraint, LocatorGrpName)                 #Re-add the Parent Constraint so the User does not have to do it again


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

        MatchTransformationsCB = QCheckBox()                                                                #Let's user decide whether or not they wish to have the transformations match when they apply the code.
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