from .legend_overlay import LegendOverlay
from .assign_materials import AssignMat
from .useful_functions import Func

class DetermType:
    """determine wheter the data is boolean or float and call assignMat and legend_overlay appropriately"""
    # class variables so things are constant between calls to legend()
    isBoolData = False
    legColor = None

    def assign(curr_legColor, matFolder, data):
        """determine type of data using minimum value of legend Paramater and calls assign_all_mats in class AssignMat appropriately"""
        DetermType.legColor = curr_legColor
        selected_prims = Func.getSelPaths()
        legParam = LegendOverlay.makeLegendParam(selected_prims, DetermType.legColor, data)

        if type(legParam['min']) == bool:
            DetermType.isBoolData = True
        else: DetermType.isBoolData = False
        AssignMat.assign_all_mats(matFolder, DetermType.legColor, data, legParam, DetermType.isBoolData)

    def legend(direction, vp_window):
        """calls make_legend_overlay with class variables so legend doesn't change color pallete or resolution if visualize doesn't update those
        so that the legend is consistent with the model colors and resolution"""
        LegendOverlay.make_legend_overlay(direction, DetermType.legColor, vp_window, DetermType.isBoolData)
