from .useful_functions import Func
from .legend_colors import AttributeColor

class AssignBoolMat:
    """class to determine color of mesh and create all materials if data is of type boolean"""

    def determColorIndex(curr_prim, dataToRead):
        """returns the index of which legend color should be used for the given curr_prim based on its attribute named dataToRead,
        I refer to the color as an index because when I create all the materials to use, they are named mat0, mat1,... (mat0 being the first color of the color palette). 
        Therefore when I assign materials, i use this colorIndex of 0,1,... to get the name of the right material to use"""
        data = curr_prim.GetAttribute(dataToRead).Get()
        if data == 'None':
            # all the data are of type String so we can handle when EnergyPlus has no results for a given entry, 
            # we assign it the last material, which is colored black to denote it has no results
            return 2
        # there are multiple ways EnergyPlus indicates a boolean result
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
        # creates 3 materials for boolean data, for True, False, and None
        for i in range(3):
            if i==2:
                # the last material's color is black
                Func.createTranspMaterial(Func.getPath(matFolder) + '/mat' + str(i), (0,0,0), ior, transmWeight, rough)
            else:
                # the legendColors.color function is also based on index, so here it create the first and last color
                Func.createTranspMaterial(Func.getPath(matFolder) + '/mat' + str(i), legendColors.color(i*(legendColors.len-1)), ior, transmWeight, rough)