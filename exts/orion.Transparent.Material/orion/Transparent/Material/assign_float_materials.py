from .useful_functions import Func
from .legend_colors import AttributeColor

class AssignFloatMat:
    
    # ------------------------------------------------------------------#
    # Sub-functions to determine color of mesh and create all materials #
    # ------------------------------------------------------------------#
    def determColorIndex(curr_prim, legendParam, dataToRead):
        """returns the index of which legend color should be used for the prim: curr_prim based on attribute named dataToRead"""
        data = curr_prim.GetAttribute(dataToRead).Get()
        if data == 'None':
            return legendParam['steps']
        floatData = float(data)
        i = 1
        # Determine which step size this data falls under based on the created legend parameters
        while(floatData>=legendParam["min"]+legendParam["step size"]*i):
            i += 1
        return i-1
    
    def createAllMats(legendColors: AttributeColor, matFolder):
        """create all materials for meshes based on legendColors, and stores them in matFolder"""
        #defining values of material properties
        ior = 1.0
        transmWeight = 0.85
        rough = 1.0
        for i in range(legendColors.len+1):
            if i==legendColors.len:
                Func.createTranspMaterial(Func.getPath(matFolder) + '/mat' + str(i), (0,0,0), ior, transmWeight, rough)
            else:
                Func.createTranspMaterial(Func.getPath(matFolder) + '/mat' + str(i), legendColors.color(i), ior, transmWeight, rough)