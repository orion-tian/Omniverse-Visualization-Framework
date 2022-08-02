from .legend_overlay import LegendOverlay
from .assign_materials import AssignMat
from .useful_functions import Func

class DetermType:
    """determine wheter to data is boolean or float and call assignMat and legend_overlay appropriately"""
    isBoolData = False
    legColor = None
    viewport_window = None
    def assign(curr_legColor, matFolder, data):
        DetermType.legColor = curr_legColor
        selected_prims = Func.getSelPaths()
        legParam = LegendOverlay.makeLegendParam(selected_prims, DetermType.legColor, data)
        print('LEGLEGLENGLENGLLEGLELGP')
        print(legParam)
        if legParam['min'] == False:
            DetermType.isBoolData = True
        else: DetermType.isBoolData = False
        AssignMat.assign_all_mats(matFolder, DetermType.legColor, data, legParam, DetermType.isBoolData)

    def legend(direction, vp_window):
        LegendOverlay.make_legend_overlay(direction, DetermType.legColor, vp_window, DetermType.isBoolData)
