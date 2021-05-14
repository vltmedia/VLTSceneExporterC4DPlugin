import c4d
import sys
import os
import json
import base64
sys.path.append(os.path.dirname(__file__))
import res.dialogs.mainDialog as MainDialog

IDC_BUTTON1 = 1000
IDC_BUTTON2= 1010
IDC_BUTTON3 = 1020
IDC_BUTTON4 = 1030
IDC_BUTTON_IMPORTVLTSCENEFILE = 1040
IDC_BUTTON_REFRESHVLTSCENEFILE = 1050
IDC_LISTVIEW_GROUPS= 1060
IDC_COMBOBOX_GROUPS= 1070
IDC_INPUTGROUPNAME_LABEL= 1080
IDC_CHECKBOX_SCENEFILEEXISTS= 1090
IDC_INPUTGROUPNAME= 1100
IDC_Group1= 1110
IDC_Group2= 1120
IDC_Group3= 1130
VLTPIPELINEPLUGIN_CMD= 1057275



class OpenVLTMainWindowCommand (c4d.plugins.CommandData) :
    def __init__(self):
        self._diag = MainDialog.MainDialog()


    def Execute(self, doc):
        
        
        self._diag.Open(c4d.DLG_TYPE_ASYNC, VLTPIPELINEPLUGIN_CMD, -1, -1, 1280, 720, 0);
        return True;


    def RestoreLayout(self, secret):

        return self._diag.RestoreLayout(VLTPIPELINEPLUGIN_CMD, 0, secret);
    





# dlg = Dialog()
# dlg.Open(c4d.DLG_TYPE_ASYNC)


def PluginStart():
    print('PluginStart')
    # if (!RegisterVLTPipelinePluginCommand()) { return false; }
    return True;

def PluginEnd():
    print('PluginEnd')

def PluginMessage( id, data):
    print('PluginMessage')
    return False;

def main():
    c4d.plugins.RegisterCommandPlugin(VLTPIPELINEPLUGIN_CMD, "VLT Pipeline Command | Scene Exporter", 0, None, 'VLT Scene Exporter', OpenVLTMainWindowCommand())
    print("VLT Pipeline Command loaded.")
    
    
if __name__ == '__main__':
    main()
