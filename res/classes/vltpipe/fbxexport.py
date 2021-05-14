import c4d
from c4d import gui, utils
import sys
import os
import json
import base64
sys.path.append(os.path.dirname(__file__))


class FBXExport:

    def __init__(self, filepath, centered, selectionOnly, asciiOut):
        self.doc = c4d.documents.GetActiveDocument()
        self.filepath = filepath;
        self.centered = centered;
        self.selectionOnly = selectionOnly;
        self.asciiOut = asciiOut;
        self.oldpos = self.doc.GetActiveObjects(0)[0].GetMg()

    # =====================================================================================================================================================
    # =====================================================================================================================================================


    def SetFirstItemAsSelected(self):
        if self.selectionOnly == True:
            items = self.doc.GetActiveObjects(0)
            items[0].SetBit(c4d.BIT_ACTIVE)
            self.doc.SetActiveObject(items[0])
            self.CenterObject()


    def SetFBXSettings(self):
        # Defines FBX export settings
        
        self.fbxExport[c4d.FBXEXPORT_ASCII] = self.asciiOut
        self.fbxExport[c4d.FBXEXPORT_SELECTION_ONLY] = True
        self.fbxExport[c4d.FBXEXPORT_TRIANGULATE] = True
        self.fbxExport[c4d.FBXEXPORT_INSTANCES] = True


    def CenterObject(self):
        if self.centered == True:
            c4d.CallCommand(1019940) # Reset PSR

    def ResetObjectToOldPosition(self):
        if self.centered == True:
            self.doc.GetActiveObjects(0)[0].SetMg(self.oldpos)



    # =====================================================================================================================================================
    # =====================================================================================================================================================

    # Call this to Export the File
    def Export(self):
        # Retrieves a path to save the exported file
        # filePath = c4d.storage.LoadDialog(title="Save File for FBX Export", flags=c4d.FILESELECT_SAVE, force_suffix="fbx")
        filePath = self.filepath
        if not filePath:
            return
        self.SetFirstItemAsSelected()
        # Retrieves FBX exporter plugin, 1026370
        fbxExportId = 1026370
        plug = c4d.plugins.FindPlugin(fbxExportId, c4d.PLUGINTYPE_SCENESAVER)
        if plug is None:
            raise RuntimeError("Failed to retrieves the fbx exporter.")

        data = dict()
        # Sends MSG_RETRIEVEPRIVATEDATA to fbx export plugin
        if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
            raise RuntimeError("Failed to retrieves private data.")

        # BaseList2D object stored in "imexporter" key hold the settings
        self.fbxExport = data.get("imexporter", None)
        if self.fbxExport is None:
            raise RuntimeError("Failed to retrieves BaseContainer private data.")

        self.SetFBXSettings()


        # Finally export the self.document
        if not c4d.documents.SaveDocument(self.doc, filePath, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, fbxExportId):
            raise RuntimeError("Failed to save the self.document.")

        print("Document successfully exported to:", filePath)
        self.ResetObjectToOldPosition()

