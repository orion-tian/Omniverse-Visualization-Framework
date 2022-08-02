from .useful_functions import Func
from .legend_colors import AttributeColor

class AssignFloatMat:
    """class to determine color of mesh and create all materials if data is of type float"""

    def determColorIndex(curr_prim, legendParam, dataToRead):
        """returns the index of which legend color should be used for the given curr_prim based on its attribute named dataToRead,
        I refer to the color as an index because when I create all the materials to use, they are named mat0, mat1,... (mat0 being the first color of the color palette). 
        Therefore when I assign materials, i use this colorIndex of 0,1,... to get the name of the right material to use"""
        data = curr_prim.GetAttribute(dataToRead).Get()
        if data == 'None':
            # return size of color pallete, which is stored in 'steps of legend paramater, to get last material 
            return legendParam['steps']
        # all data is of type String so convert to float to use it in calculations
        floatData = float(data)
        i = 1
        # Determine which step size this data falls under based on legend parameters
        while(floatData>=legendParam["min"]+legendParam["step size"]*i):
            i += 1
        return i-1
    
    def createAllMats(legendColors: AttributeColor, matFolder):
        """create all materials for meshes based on legendColors, and stores them in matFolder"""
        for i in range(legendColors.len+1):
            if i==legendColors.len:
                # the last material to use if data is 'None', colored black
                Func.createTranspMaterial(Func.getPath(matFolder) + '/mat' + str(i), (0,0,0))
            else:
                # legendColors.color also uses an index system so 0 to its length-1 creates all the colors in its color palette
                Func.createTranspMaterial(Func.getPath(matFolder) + '/mat' + str(i), legendColors.color(i))