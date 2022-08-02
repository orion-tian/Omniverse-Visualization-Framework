from .useful_functions import Func
from .legend_colors import AttributeColor

class AssignBoolMat:
    
    # ------------------------------------------------------------------#
    # Sub-functions to determine color of mesh and create all materials #
    # ------------------------------------------------------------------#
    def determColorIndex(curr_prim, dataToRead):
        """returns the index of which legend color should be used for the prim: curr_prim based on attribute named dataToRead"""
        data = curr_prim.GetAttribute(dataToRead).Get()
        if data == 'None':
            return 2
        if data == 'True' or data=='Yes' or data=='yes' or data=='Y' or data=='y':
            return 1
        else:
            return 0
    
    def createAllMats(legendColors: AttributeColor, matFolder):
        """create all materials for meshes based on legendColors, and stores them in matFolder"""
        #defining values of material properties
        ior = 1.0
        transmWeight = 0.85
        rough = 1.0
        for i in range(3):
            if i==2:
                Func.createTranspMaterial(Func.getPath(matFolder) + '/mat' + str(i), (0,0,0), ior, transmWeight, rough)
            else:
                Func.createTranspMaterial(Func.getPath(matFolder) + '/mat' + str(i), legendColors.color(i*(legendColors.len-1)), ior, transmWeight, rough)