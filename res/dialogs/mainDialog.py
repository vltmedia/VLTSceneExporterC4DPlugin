import c4d
from c4d import gui, utils
import shutil
import sys
import os
import json
import base64
from pathlib import Path


from .spawnCategoryDialog import SpawnCategoryDialog
from ..classes.vltpipe.scene import VLT_Scene
from ..classes.vltpipe.sceneexport import VLT_SelectedGeoExport as VLT_SelectedGeoExport

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
IDC_EXPORTSELECTEDBUTTON= 1150
IDC_CHECKBOXINSTANCESPACENAME= 1160
IDC_CHECKBOXINSTANCEDOTNAME= 1170
IDC_CHECKBOXUSEOVERIDENAME= 1180
IDC_CHECKBOXFBXEXPORT= 1200
IDC_BUTTON_REFRESHVLTSCENEFILECATEGORYLIST= 1190
VLTPIPELINEPLUGIN_CMD= 1057275
VLTPIPELINESCENEEXPORTPLUGIN_CMD= 1057276

class MainDialog(c4d.gui.GeDialog):

    GRP_FOLDABLE = 1000
    EDTOMEFIELD = 1001

    def __init__(self):
        super(MainDialog, self).__init__()
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
        self.AddButton(IDC_BUTTON_CLEARVLTSCENEFILE, c4d.BFH_SCALEFIT|c4d.BFH_LEFT, 150, 20, "Delete VLT Pipe Scene File")
        self.GroupEnd()
        
        
    def CreateGroupSettingsRow(self):
        self.GroupBegin(0, c4d.BFV_FIT | c4d.BFH_SCALEFIT, 2, 0, "Category Settings", 0) 
        self.GroupBorderSpace(5, 5, 5, 5)
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        
        self.GroupBegin(0, c4d.BFV_FIT | c4d.BFH_SCALEFIT, 2, 0, "Overide Settings", 0) 
        self.GroupBorderSpace(5, 5, 5, 5)
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.AddCheckbox(IDC_CHECKBOXUNIQUENAME, c4d.BFH_SCALE, 150, 20, "Force Unique Name")
        self.AddCheckbox(IDC_CHECKBOXINSTANCESPACENAME, c4d.BFH_SCALE, 150, 20, "Instance = ' ' (space)")
        self.AddCheckbox(IDC_CHECKBOXINSTANCEDOTNAME, c4d.BFH_SCALE, 150, 20, "Instance = '.' (period)")
        self.AddCheckbox(IDC_CHECKBOXUSEOVERIDENAME, c4d.BFH_SCALE, 150, 20, "Use Overide Category Name")
        self.AddCheckbox(IDC_CHECKBOXFBXEXPORT, c4d.BFH_SCALE, 150, 20, "Export FBX")
        self.GroupEnd()
        
        self.GroupBegin(0, c4d.BFV_FIT | c4d.BFH_SCALEFIT, 2, 0, "Category Overide Settings", 0) 
        self.GroupBorderSpace(5, 5, 5, 5)
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.AddStaticText(IDC_INPUTGROUPNAME_LABEL, c4d.BFH_SCALEFIT | c4d.BFH_LEFT, 30, 20, "Category Name", c4d.BORDER_BLACK)
        self.AddEditText(IDC_INPUTGROUPNAME, c4d.BFH_SCALEFIT | c4d.BFH_RIGHT, 80, 20)
        self.AddButton(IDC_BUTTON_REFRESHVLTSCENEFILE, c4d.BFH_SCALEFIT|c4d.BFH_LEFT, 150, 20, "Refresh Guess From Selected In Scene")
        self.AddButton(IDC_BUTTON_REFRESHVLTSCENEFILECATEGORYLIST, c4d.BFH_SCALEFIT|c4d.BFH_LEFT, 150, 20, "Refresh From Selected In Category List")
        
        self.GroupEnd()
        
        
        self.GroupEnd()

        
        
        # self.CreateGroupListRow()
        
                
    def CreateGroupListRow(self):
        self.GroupBegin(0, c4d.BFV_FIT | c4d.BFH_SCALEFIT, 2, 0, "Category List", 0) 
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
        self.AddButton(IDC_BUTTON1, c4d.BFH_SCALEFIT|c4d.BFH_LEFT, 150, 20, "Spawn Objects Menu")
        self.AddButton(IDC_EXPORTSELECTEDBUTTON, c4d.BFH_SCALEFIT|c4d.BFH_LEFT, 150, 20, "Export Selected")
        self.GroupEnd()
        
    def SetupMainLayout(self):
        self.CreateDependenciesRow()
        self.CreateGroupSettingsRow()
        self.SetPaths()
        self.CreateGroupNextRow()
        
        
    def CreateLayout(self):
        
        self.SetTitle("VLT Pipeline")
        self.SetupMainLayout()
        return True
    
    def CreateGroupListRow(self):
        self.GroupBegin(0, c4d.BFV_FIT | c4d.BFH_SCALEFIT, 2, 0, "Category List", 0) 
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
            self.CreateGroupListRow()

    def SetPaths(self):
        filee = os.path.dirname(__file__)
        path = Path(filee).parent.absolute()
        self.dirpath = path
        self.doc = c4d.documents.GetActiveDocument()
        self.SceneFilePath = self.GetCurrentScenePath() +"/"+self.GetCurrentSceneName()+".scene"
        self.PartsPath = self.GetCurrentScenePath() +"/parts"
        self.CheckSceneFileExists()

    def GetComboboxSelected(self):
        print(int(self.GetInt32(IDC_COMBOBOX_GROUPS) / 100))
        print('self.Scene.Categories', self.Scene.Categories)
        return self.Scene.Categories[int(self.GetInt32(IDC_COMBOBOX_GROUPS) / 100)]

    def GetGroupName(self):
        delim = '&^'
        if self.GetBool(IDC_CHECKBOXINSTANCESPACENAME) == True:
            delim = ' '
            
        if self.GetBool(IDC_CHECKBOXINSTANCEDOTNAME) == True:
            delim = '.'
            
        namee = c4d.documents.GetActiveDocument().GetActiveObjects(0)[0].GetName()
        if delim in namee:
            updatedname = namee.split(delim)[0]
            namee = updatedname
        return namee.replace('.', '_')

    def SetGroupName(self):
        
        groupname = c4d.documents.GetActiveDocument().GetActiveObjects(0)[0].GetName()
        if self.GetBool(IDC_CHECKBOXINSTANCEDOTNAME) == True:
            groupname = groupname.split('.')[0]

        if self.GetBool(IDC_CHECKBOXUSEOVERIDENAME) == True:
            groupname = self.GetString(IDC_INPUTGROUPNAME)

        if self.GetBool(IDC_CHECKBOXINSTANCESPACENAME) == True:
            groupname = groupname.split(' ')[0]


            
        self.VLT_SelectedGeoExport_.SetGroupName(groupname)

    def ImportSceneFile(self):
        fn = c4d.storage.LoadDialog(0, 'Select a VLT .scene File')
        shutil.copy(fn, self.GetCurrentScenePath() +"/"+self.GetCurrentSceneName()+".scene")
        self.SetPaths()


    def Command(self, wid, msg):
        
        if wid == IDC_BUTTON_IMPORTVLTSCENEFILE:
            print('IDC_BUTTON_IMPORTVLTSCENEFILE Clicked')
            self.ImportSceneFile()
            # f = open(fn.decode("utf-8"))

        if wid == IDC_BUTTON_CLEARVLTSCENEFILE:
            print('IDC_BUTTON_CLEARVLTSCENEFILE Clicked')
            if os.path.exists(self.SceneFilePath):
                os.remove(self.GetCurrentScenePath() +"/"+self.GetCurrentSceneName()+".scene")
                gui.MessageDialog('Deleted the VLTScene file at | ' + self.GetCurrentScenePath() +"/"+self.GetCurrentSceneName()+".scene")
            else:
                gui.MessageDialog('No VLTScene file exists at | ' + self.GetCurrentScenePath() +"/"+self.GetCurrentSceneName()+".scene")

        if wid == IDC_BUTTON_REFRESHVLTSCENEFILE:
            print('IDC_BUTTON_REFRESHVLTSCENEFILE Clicked')
            self.SetString(IDC_INPUTGROUPNAME, self.GetGroupName())
                    
        if wid == IDC_BUTTON_REFRESHVLTSCENEFILECATEGORYLIST:
            print('IDC_BUTTON_REFRESHVLTSCENEFILE Clicked')
            self.SetString(IDC_INPUTGROUPNAME, self.GetComboboxSelected())
                    
        if wid == IDC_EXPORTSELECTEDBUTTON:
            print('IDC_EXPORTSELECTEDBUTTON Clicked')
            self.VLT_SelectedGeoExport_ = VLT_SelectedGeoExport(self.GetBool(IDC_CHECKBOXUNIQUENAME))
            self.VLT_SelectedGeoExport_.FBXExport = self.GetBool(IDC_CHECKBOXFBXEXPORT)
            self.SetGroupName()
            self.VLT_SelectedGeoExport_.ExecuteProcess()
            
        if wid == IDC_BUTTON1:
            self.SpawnCategoryDialog_ = SpawnCategoryDialog()
            self.SpawnCategoryDialog_.Open(c4d.DLG_TYPE_ASYNC, VLTPIPELINESCENEEXPORTPLUGIN_CMD, -1, -1, 640, 360, 0)
            
            
        if wid == IDC_BUTTON2:
            self.SpawnCategoryDialog_ = SpawnCategoryDialog()
            self.SpawnCategoryDialog_.Open(c4d.DLG_TYPE_ASYNC, VLTPIPELINESCENEEXPORTPLUGIN_CMD, -1, -1, 1280, 720, 0)
            print('IDC_BUTTON2 Clicked')
            
        if wid == c4d.DLG_CANCEL:
            self.Close()
        return True


