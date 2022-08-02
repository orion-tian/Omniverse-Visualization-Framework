import omni.ui as ui
import omni.usd
import omni.kit.commands
from pxr import Sdf

class Func:
    """class containing frequently used functions or ones that take up a lot of space"""
    #--------------#
    # UI Functions #
    #--------------#
    def makeComboAndLabel(label, dict):
        """Creates a ui label with given string label and a comboBox underneath with the keys in given dict, and
        returns a reference to the created comboBox"""
        magicNumHeight = 30
        magicNumWidth = 300

        ui.Label(label, height=magicNumHeight, style = {"font_size":16})

        comboBox = ui.ComboBox(width=magicNumWidth, height=magicNumHeight)
        for key in dict:
            comboBox.model.append_child_item(None, ui.SimpleStringModel(key))
        return comboBox

    def getComboValue(comboBox, dict):
        """returns the value associated with the chosen key of the comboBox in dict"""
        index = comboBox.model.get_item_children()[comboBox.model.get_item_value_model().get_value_as_int()]
        return dict[comboBox.model.get_item_value_model(index).as_string]
    
    #---------------#
    # USD Functions #
    #---------------#
    def defineXform(path):
        """returns a reference to the created Xform with prim path of path"""
        return omni.usd.get_context().get_stage().DefinePrim(path, 'Xform')

    def getPrimAtPath(path):
        """returns the prim at the given path"""
        return omni.usd.get_context().get_stage().GetPrimAtPath(path)
    
    def getPath(prim):
        """returns the path of the given prim as a string"""
        return prim.GetPath().pathString 
    
    def getSelPaths():
        """returns the list of currently selected prim paths"""
        return omni.usd.get_context().get_selection().get_selected_prim_paths()

    def setSelPaths(pathList):
        """sets the selected prim paths as the paths in pathList"""
        omni.usd.get_context().get_selection().set_selected_prim_paths(pathList, False)
    
    def invisible(pathList):
        """makes the prims in pathList invisible"""
        for path in pathList:
            prim = Func.getPrimAtPath(path)
            if prim.GetAttribute('visibility').Get()=='inherited':
                omni.kit.commands.execute('ToggleVisibilitySelectedPrims',selected_paths=pathList)
    
    def createTranspMaterial(matFolderString, color):
        """create a transparent material in xForm given by matFolderString with properties given by the arguments"""
        # material properties
        ior = 1.0
        transmWeight = 0.7
        rough = 1.0
        # Create material
        omni.kit.commands.execute('CreateMdlMaterialPrim',
                                mtl_url='OmniSurface.mdl',
                                mtl_name='OmniSurface',
                                mtl_path=matFolderString,
                                select_new_prim=False)
        # Change material properties
        mtl_prim = Func.getPrimAtPath(matFolderString)
        omni.usd.create_material_input(mtl_prim, "diffuse_reflection_color", color, Sdf.ValueTypeNames.Color3f),
        omni.usd.create_material_input(mtl_prim, "specular_reflection_ior", ior, Sdf.ValueTypeNames.Float)
        omni.usd.create_material_input(mtl_prim, "enable_specular_transmission", True, Sdf.ValueTypeNames.Bool)
        omni.usd.create_material_input(mtl_prim, "specular_transmission_weight", transmWeight, Sdf.ValueTypeNames.Float)
        omni.usd.create_material_input(mtl_prim, "specular_reflection_roughness", rough, Sdf.ValueTypeNames.Float)