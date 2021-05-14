import c4d
from c4d import gui, utils
import sys
import os
import json
import base64
from .fbxexport import FBXExport as FBXExport
sys.path.append(os.path.dirname(__file__))




class VLT_SelectedGeoExport:

    def __init__(self, unique):
        self.outjs = {"Objects" :[], "Categories" :[], "Count" : 0}
        self.fbxscenefile = {"Objects" :[], "Categories" :[], "Count" : 0}
        self.unique = unique
        self.OverideGroupName = False
        self.FBXExport = False
        self.doc = c4d.documents.GetActiveDocument()

    def GetUniqueId(self):
        return base64.b64encode(os.urandom(4)).decode('ascii').replace('=', 'uw').replace('+', 'ouo').replace('-', 'onJ').replace('/', 's')
    
    def getGlobalPosition(self, obj):
        return obj.GetMg().off

    def getGlobalRotation(self, obj):
        return utils.MatrixToHPB(obj.GetMg())

    def getGlobalScale(self, obj):
        m = obj.GetMg()
        return c4d.Vector(m.v1.GetLength(),
                            m.v2.GetLength(),
                            m.v3.GetLength())
    def GetSelectedObjects(self):
        return self.doc.GetActiveObjects(0)

    def WriteDictToFile(self, outdict, filepath, writeState):
        print(outdict)
        with open(filepath, writeState) as json_file:
            json.dump(outdict, json_file)
        print("Completed Writing File to Disk! | ", filepath)

    def GetCurrentScenePath(self):
        return self.doc.GetDocumentPath()

    def GetCurrentSceneName(self):
        return os.path.splitext(self.doc.GetDocumentName())[0]


    def GetObjectsTransform(self, obj):

        # location = obj.GetMg()
        Position = [self.getGlobalPosition(obj)[0],self.getGlobalPosition(obj)[1],self.getGlobalPosition(obj)[2]]
        Rotation = [self.getGlobalRotation(obj)[0],self.getGlobalRotation(obj)[1],self.getGlobalRotation(obj)[2]]
        Scale = [self.getGlobalScale(obj)[0],self.getGlobalScale(obj)[1],self.getGlobalScale(obj)[2]]
        Transform = {'Position':Position, 'Rotation':Rotation, 'Scale':Scale }
        namee = obj.GetName()
        category = namee.replace('.', '_')
        if self.unique == True:
            nameupdate = namee + '_'+ self.GetUniqueId()
            namee = nameupdate
        nameup = namee.replace('.', '_')
        namee = nameup
        if ' ' in namee:
            category = namee.split(' ')[0]
        if self.OverideGroupName == True:
            category = self.GroupName.replace('.', '_')
        outjs = {"Name": nameup,"Category": category.replace('.', '_'), "Transform" : Transform}
        if category not in self.outjs['Categories']:
            self.outjs['Categories'].append(category)
        if category not in self.fbxscenefile['Categories']:
            self.fbxscenefile['Categories'].append(category.replace('.', '_'))
        return outjs


    def GetSceneConfigPath(self):
        return self.GetCurrentScenePath() +"/"+self.GetCurrentSceneName()+".scene"


    def GetObjectFBXPath(self):
        objectname = self.GroupName
        # objectname = self.doc.GetActiveObjects(0)[0].GetName()
        # if ' ' in objectname:
        objectnameupdate = objectname
        objectname = objectnameupdate
        self.fbxfolderpath = self.GetCurrentScenePath() +"/parts/"+objectname.replace('.', '_')
        self.fbxpath =  self.fbxfolderpath +"/"+objectname.replace('.', '_')+".fbx"
        self.fbxScenepath =  self.fbxfolderpath +"/"+objectname.replace('.', '_')+".scene"
        
        if os.path.exists(self.GetCurrentScenePath() +"/parts") == False:
            os.makedirs(self.GetCurrentScenePath() +"/parts")
        
        if os.path.exists(self.fbxfolderpath) == False:
            os.makedirs(self.fbxfolderpath)
        
        return self.fbxpath


    def CheckSceneConfigStatus(self):
        return os.path.exists( self.GetCurrentScenePath() +"/"+self.GetCurrentSceneName()+".scene")

    def HandleSceneConfigCreation(self):
        if self.CheckSceneConfigStatus() == True:
            with open(self.GetSceneConfigPath()) as f:
                try:
                    data = json.load(f)
                    self.outjs = data
                except Exception as e:
                    print(e)

    def AddItemsToObjectsList(self):
        # Get Selected Items In Scene
        self.items = self.GetSelectedObjects()
        
        # Iterate through items
        for obj in self.items:
            # Get the Transform info per the object
            js = self.GetObjectsTransform(obj)
            found = False
            for subobj in self.outjs['Objects']:
                if subobj['Name'] == obj.GetName():
                    subobj['Transform'] = js
                    found = True
            if found == False:
                # Add the Transform dict to the Objects list inside of the OutputJs
                self.outjs['Objects'].append(js)
          
                    
            self.fbxscenefile['Objects'].append(js)
        # Set the Count of the Objects inside of the OutputJs
        self.outjs["Count"] = len(self.outjs['Objects'])
        self.fbxscenefile["Count"] = len(self.fbxscenefile['Objects'])

    
    def WriteFBXFile(self):
        fbxpath = self.GetObjectFBXPath()
        FBXExport_ = FBXExport(fbxpath, True, True, False)
        FBXExport_.Export()
            
    def SetGroupName(self, groupname):
        self.OverideGroupName = True
        self.GroupName = groupname

        

    def ExecuteProcess(self):
        # Check if Scene Config Exists in the same directory path as the C4D Scene file. Sets self.outjs to the JSON inside of the .scene file.
        self.HandleSceneConfigCreation()

        # Get Selected Items In Scene
        self.AddItemsToObjectsList()

        # Create/update the Scene Output JSON file
        self.WriteDictToFile(self.outjs,self.GetSceneConfigPath(),'w')
        fbxpath = self.GetObjectFBXPath()
        if self.FBXExport == True:
        # Write FBX file and the .scene file for that object and instances.
            self.WriteFBXFile()
        self.WriteDictToFile(self.fbxscenefile,self.fbxScenepath,'w')
        gui.MessageDialog('Finished Writing the .scene file and Scene Object to file!')
        print(self.outjs)

    def RestoreLayout(self):
        gui.MessageDialog(self.GetSceneConfigPath())

    def RunTest(self):
        gui.MessageDialog(self.GetSceneConfigPath())




# ==================================================================================================================
# ==================================================================================================================
# ==================================================================================================================



# # Main function
# def main():
#     SelectedGeoExport_ = SelectedGeoExport(True)
#     SelectedGeoExport_.ExecuteProcess()

# # Execute main()
# if __name__=='__main__':
#     main()