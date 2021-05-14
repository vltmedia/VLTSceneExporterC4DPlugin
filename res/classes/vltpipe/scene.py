
import json


class VLT_Scene:

  def __init__(self):
    self.Loaded = True;
  
  def LoadFromFile(self, filepath):
    self.filepath = filepath
    data = {}
    with open(filepath) as f:
      data = json.load(f)
    self.SceneData = data
    self.Categories = data['Categories']
    self.Objects = data['Objects']
    print(self.SceneData)
    print('Categories', self.Categories)
    
  def GetCategories(self):
    return self.Categories
  def GetObjects(self):
    return self.Objects

    
  def GetObjectCount(self):
    return len(self.Objects)
  
  def FilterObjectsCategory(self, selectedtext):
    outarray = []
    for obj in self.Objects:
        if obj['Category'] == selectedtext:
            outarray.append(obj)
    return outarray

    
