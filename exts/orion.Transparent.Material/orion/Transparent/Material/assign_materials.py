import omni.usd
from pxr import UsdShade

from .assign_float_materials import AssignFloatMat
from .assign_bool_materials import AssignBoolMat
from .useful_functions import Func

class AssignMat:
    # ----------------------------------------------------#
    # Functions to assign meshes the appropriate material #
    # ----------------------------------------------------#
    isBoolData = False
    # Assign material to visualize energy results to all selected meshes
    def assign_all_mats(matFolder, legendColors, dataToRead, legendParam, isBoolData):
        """assign material to visualize energy results of attribute dataToRead of selected results, matFolder is where to find the materials"""
        # create all materials to use based on whether it's boolean or float data
        AssignMat.isBoolData = isBoolData
        if AssignMat.isBoolData:
            AssignBoolMat.createAllMats(legendColors, matFolder)
        else:
            AssignFloatMat.createAllMats(legendColors, matFolder)
        # process to make colored volume
        selected_prims = Func.getSelPaths()
        for s in selected_prims:
            # determine if s is prim or layer and act accordingly 
            curr_prim = Func.getPrimAtPath(s)
            if len(curr_prim.GetChildren())==0:
                if isBoolData:
                    color = AssignBoolMat.determColorIndex(curr_prim, dataToRead)
                else:
                    color = AssignFloatMat.determColorIndex(curr_prim, legendParam, dataToRead)
                volmFolder = Func.getPrimAtPath('/World/Energy_Results/ColoredVolms')           
                AssignMat.assign_material(s, color, volmFolder, matFolder)
            else:
                volmFolder = Func.defineXform('/World/Energy_Results/ColoredVolms/' + curr_prim.GetName())
                AssignMat.assign_one_layer_mats(curr_prim.GetChildren(), volmFolder, matFolder, legendParam, dataToRead)
            # make original selection invisible to better view energy results
            Func.invisible([s])

    def assign_one_layer_mats(children, volmFolder, matFolder, legendParam, dataToRead):
        """recursive helper method to assign materials for one layer, children are the list of children of the layer"""
        if len(children)==0:
            return
        for c in children:
                if len(c.GetChildren()) == 0:
                    # Determine color of the prim, 
                    # assign a copied prim a transparent material of that color
                    if AssignMat.isBoolData:
                        color = AssignBoolMat.determColorIndex(c, dataToRead)     
                    else:
                        color = AssignFloatMat.determColorIndex(c, legendParam, dataToRead)           
                    AssignMat.assign_material(Func.getPath(c), color, volmFolder, matFolder)
                else:
                    # c is a layer so create a folder in energy Results for that layer then traverse it
                    subVolmFolder = Func.defineXform(Func.getPath(volmFolder) + '/' + c.GetName())
                    AssignMat.assign_one_layer_mats(c.GetChildren(), subVolmFolder, matFolder, legendParam, dataToRead)

    # Assign material to one prim
    def assign_material(prim_path, colorIndex, volmsFolder, matFolder):
        """assign the material corresponding with colorIndex to the prim at prim_path and store the resulting colored volume in volmsFolder"""
        #copy prim
        omni.kit.commands.execute('CopyPrim',
                                path_from=prim_path,
                                path_to=prim_path+'ColoredVolm',
                                exclusive_select=False)
        #change selected prim paths from selected layer to this copied prim to bind material
        Func.setSelPaths([prim_path+"ColoredVolm"])
        #get the created material
        mtl_prim = Func.getPrimAtPath(Func.getPath(matFolder) + '/mat' + str(colorIndex))

        # Get the path to the prim
        prim = Func.getPrimAtPath(prim_path+'ColoredVolm')
        prim_name = prim.GetName()
        # Bind the material to the prim
        mat_shade = UsdShade.Material(mtl_prim)
        UsdShade.MaterialBindingAPI(prim).Bind(mat_shade, UsdShade.Tokens.strongerThanDescendants)
        # Move colored volume to the appropriate folder
        omni.kit.commands.execute('MovePrim',
                                path_from=prim_path+'ColoredVolm',
                                path_to=Func.getPath(volmsFolder) + '/' + prim_name)  
    