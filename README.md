# Description

A Cinema 4D plugin that aids in the exporting of object transform data to an agnostic file type and schema. 



# Schema

### Example:

```json
{"Objects": [{"Name": "ObjectThing", "Category": "RING1.1", "Transform": {"Position": [0, 0, 0], "Rotation": [0, 0, 0], "Scale": [0, 0, 0]}}], "Categories": ["RING1.1"], "Count": 1}
```



# Usage

## Scene Exporter

1. Select the objects to export that share the same base geometry. Examples include, Instances, similar geometry, copy & pasted geometry, etc.
2. Chose one of the Checkboxes in the `Overide Settings` area if needed.
   - If you chose one of the `Instance = ...` checkboxes,  click the `Refresh Gues From Selected In Scene` button to have the `Category Name` text field fill in with what the program thinks the category name should be based on your Checkbox choices
   - If you chose `Use Overide Category Name`, set the category name in the `Category Name` text field. This will be used in the scene file.
3. Click `Export Selected` button to export every selected object's Transform information, along with an fbx file containing the **<u>FIRST SELECTED OBEJCT</u>** with it's Transform reset to center for LOD and other work.
4. Do this again for other objects.

## Scene Importer

1. Make sure you have a .scene file associated with your .c4d file. Use the `Import VLT Pipe Scene File` if needed.
2. Click the `Spawn Objects Menu` to open up the Import menu
3. Select a Category from the Dropdown list.
4. Select an object in your scene to use as the object to either duplicate or instance based on the Objects in your chosen Category.
5. Click the appropriate button based on if you want Instances of the selected object, or just plain duplicated objects.
6. Do this for each Category.



# Roadmap

- Full Scene setup.