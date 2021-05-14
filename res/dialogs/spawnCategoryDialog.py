import c4d
from c4d import gui, utils
import sys
import os
import json
import base64
from pathlib import Path

from ..classes.vltpipe.scene import VLT_Scene

IDC_BUTTON1 = 1000
IDC_BUTTON2= 1010
IDC_BUTTON3 = 1020
IDC_BUTTON4 = 1030
IDC_BUTTON_IMPORTVLTSCENEFILE = 1040
IDC_BUTTON_REFRESHVLTSCENEFILE = 1050
IDC_BUTTON_CLEARVLTSCENEFILE = 1051
IDC_LISTVIEW_GROUPS= 1060
IDC_COMBOBOX_GROUPS= 1070
IDC_INPUTGROUPNAME_LABEL= 1080
IDC_CHECKBOX_SCENEFILEEXISTS= 1090
IDC_INPUTGROUPNAME= 1100
IDC_Group1= 1110
IDC_Group2= 1120
IDC_Group3= 1130
IDC_CHECKBOXUNIQUENAME= 1140


class SpawnCategoryDialog(c4d.gui.GeDialog):

    GRP_FOLDABLE = 1000
    EDTOMEFIELD = 1001

    def __init__(self):
        super(SpawnCategoryDialog, self).__init__()
        self.__foldindex = 10000
        self.__folduas = {}
        

    def CreateDependenciesRow(self):
        self.GroupBegin(0, c4d.BFV_FIT|c4d.BFH_SCALEFIT, 2, 0, "Dependencies", 0) 
        self.GroupBorderSpace(5, 5, 5, 5)
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.AddCheckbox(IDC_CHECKBOX_SCENEFILEEXISTS, c4d.BFH_SCALE|c4d.BFV_TOP, 150, 20, "Config Exists")
        self.GroupEnd()
        
        self.GroupBegin(0, c4d.BFV_BOTTOM|c4d.BFH_SCALEFIT, 2, 0, "Scene File", 0) 
        self.GroupBorderSpace(5, 5, 5, 5)
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.AddButton(IDC_BUTTON_IMPORTVLTSCENEFILE, c4d.BFH_SCALEFIT|c4d.BFH_LEFT, 150, 20, "Import VLT Pipe Scene File")
        self.AddButton(IDC_BUTTON_REFRESHVLTSCENEFILE, c4d.BFH_SCALEFIT|c4d.BFH_LEFT, 150, 20, "Refresh VLT Pipe Scene File")
        self.AddButton(IDC_BUTTON_CLEARVLTSCENEFILE, c4d.BFH_SCALEFIT|c4d.BFH_LEFT, 150, 20, "Delete VLT Pipe Scene File")
        self.GroupEnd()
        
        
    def CreateGroupSettingsRow(self):
        self.GroupBegin(0, c4d.BFV_FIT | c4d.BFH_SCALEFIT, 2, 0, "Group Settings", 0) 
        self.GroupBorderSpace(5, 5, 5, 5)
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        
        self.GroupBegin(0, c4d.BFV_FIT | c4d.BFH_SCALEFIT, 2, 0, "Settings 2", 0) 
        self.GroupBorderSpace(5, 5, 5, 5)
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.AddCheckbox(IDC_CHECKBOXUNIQUENAME, c4d.BFH_SCALE, 150, 20, "Unique Name")
        self.GroupEnd()
        
        self.GroupBegin(0, c4d.BFV_FIT | c4d.BFH_SCALEFIT, 2, 0, "Settings 3", 0) 
        self.GroupBorderSpace(5, 5, 5, 5)
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.AddStaticText(IDC_INPUTGROUPNAME_LABEL, c4d.BFH_SCALEFIT | c4d.BFH_LEFT, 30, 20, "Group Name", c4d.BORDER_BLACK)
        self.AddEditText(IDC_INPUTGROUPNAME, c4d.BFH_SCALEFIT | c4d.BFH_RIGHT, 80, 20)
        self.GroupEnd()
        
        
        self.GroupEnd()
        self.SetPaths()
        
        
        
                
    def CreateGroupListRow(self):
        self.GroupBegin(0, c4d.BFV_FIT | c4d.BFH_SCALEFIT, 2, 0, "Group List", 0) 
        self.GroupBorderSpace(5, 5, 5, 5)
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.AddComboBox(IDC_COMBOBOX_GROUPS, c4d.BFH_SCALEFIT | c4d.BFH_RIGHT, 80, 20)
        Categories = self.Scene.GetCategories()
        comboid = 0
        comboidadd = 100
        for category in Categories:
            self.AddChild(IDC_COMBOBOX_GROUPS, comboid, category)
            comboid += comboidadd
        self.GroupEnd()
        
        self.CreateGroupNextRow()
        
                        
    def CreateGroupNextRow(self):
        self.GroupBegin(0, c4d.BFV_SCALEFIT | c4d.BFH_SCALEFIT, 2, 0, "Test Group", 0) 
        self.GroupBorderSpace(5,5,5,5)
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.AddButton(IDC_BUTTON1, c4d.BFH_SCALEFIT|c4d.BFH_LEFT, 150, 20, "Spawn Instances Based on Selected Object")
        self.AddButton(IDC_BUTTON2, c4d.BFH_SCALEFIT|c4d.BFH_LEFT, 150, 20, "Spawn by Duplicating Selected Object")
        self.GroupEnd()
        
    def SetupMainLayout(self):
        self.SetPaths()
        self.CreateGroupListRow()

        
        
        
    def CreateLayout(self):
        
        self.SetTitle("VLT Pipeline")
        self.SetupMainLayout()
        return True


    def GetCurrentSceneName(self):
        return os.path.splitext(self.doc.GetDocumentName())[0]


    def GetCurrentScenePath(self):
        return self.doc.GetDocumentPath()

    def GetSceneConfigPath(self):
        self.SetPaths()
        return self.GetCurrentScenePath() +"/"+self.GetCurrentSceneName()+".scene"

    def CheckSceneFileExists(self):
        self.SceneFileExists = os.path.exists(self.SceneFilePath)
        self.SetBool(IDC_CHECKBOX_SCENEFILEEXISTS, self.SceneFileExists)
        if self.SceneFileExists == True:
            self.Scene = VLT_Scene()
            self.Scene.LoadFromFile(self.SceneFilePath)

    def SetPaths(self):
        filee = os.path.dirname(__file__)
        path = Path(filee).parent.absolute()
        self.dirpath = path
        self.doc = c4d.documents.GetActiveDocument()
        self.SceneFilePath = self.GetCurrentScenePath() +"/"+self.GetCurrentSceneName()+".scene"
        self.PartsPath = self.GetCurrentScenePath() +"/parts"
        self.CheckSceneFileExists()

    def GetComboboxSelected(self):
        return self.Scene.Categories[int(self.GetInt32(IDC_COMBOBOX_GROUPS) / 100)]

    def FilterObjects(self):
        selectedtext = self.GetComboboxSelected()
        self.outarray = self.Scene.FilterObjectsCategory(selectedtext)
        print(self.outarray)
    
    def GetSelectedObject(self):
        return c4d.documents.GetActiveDocument().GetActiveObjects(0)[0]
    
    def SpawnObjects(self):
        self.doc.InsertObject(c4d.BaseObject(c4d.Onull))
        parent = self.doc.SearchObject("Null")
        parent.SetName(self.GetComboboxSelected())
        InstanceMode = True
        self.FilterObjects()
        
        self.baseobject = self.GetSelectedObject()
        for obj in self.outarray:
            if InstanceMode == True:
                c4d.CallCommand(5126)
            else:
                c4d.CallCommand(12107) # Copy
                c4d.CallCommand(12108) # Paste
            position = obj['Transform']['Position']
            rotation = obj['Transform']['Rotation']
            scale = obj['Transform']['Scale']
            self.currentinstance = self.GetSelectedObject()
            self.currentinstance.SetAbsPos(c4d.Vector(position[0], position[1], position[2]))
            self.currentinstance.SetAbsRot(c4d.Vector(rotation[0], rotation[1], rotation[2]))
            self.currentinstance.SetAbsScale(c4d.Vector(scale[0], scale[1], scale[2]))
            self.currentinstance.InsertUnder(parent)
            
            self.baseobject.SetBit(c4d.BIT_ACTIVE)
            self.doc.SetActiveObject(self.baseobject)
            
            
        c4d.EventAdd()     
        
        

    def Command(self, wid, msg):
        
        if wid == IDC_BUTTON_IMPORTVLTSCENEFILE:
            print('IDC_BUTTON_IMPORTVLTSCENEFILE Clicked')
            
        if wid == IDC_BUTTON1:
            print('IDC_BUTTON1 Clicked')
            self.InstanceMode = True
            self.SpawnObjects()
            
        if wid == IDC_BUTTON2:
            print('IDC_BUTTON2 Clicked')
            self.InstanceMode = False
            self.SpawnObjects()
            
        if wid == c4d.DLG_CANCEL:
            self.Close()
        return True


