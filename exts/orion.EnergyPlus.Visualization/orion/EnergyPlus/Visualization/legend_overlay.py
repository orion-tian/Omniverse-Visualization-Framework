from omni.ui import scene as sc
from .useful_functions import Func

class LegendOverlay:
    """render legend onto viewport"""
    #---------------------------------------#
    # Functions to create Legend Paramaters #
    #---------------------------------------#
    def makeLegendParam(selected_prims, legendColors, dataToFind):
        """returns a dictionary containg the min, max, step (number of legend colors), and step size (data range of each legend piece) of the data 
        found in attribute dataToFind of the selected_prims"""
        # Create a list of all data in the custom attribute dataToFind in selected prims
        dataList = LegendOverlay.findData(selected_prims, dataToFind)
        # Create legend paramater 
        legendParam = {}
        legendParam.update({"min" : min(dataList)})
        legendParam.update({"max" : max(dataList)})
        legendParam.update({"steps" : legendColors.len})
        legendParam.update({"step size" : (max(dataList)+1-min(dataList))/legendColors.len})

        return legendParam 
    
    def findData(selected_prims, dataToFind):
        """returns a list of all the data in attribute dataToFind in the selected_prims, 
        if data is 'None', it leaves it out of the list so that functions min and max work in makeLegendParam()"""
        tmp = []
        for s in selected_prims:
            curr_prim = Func.getPrimAtPath(s)
            # determine if s is a mesh or layer, has assumption that a prim with children is not a mesh, not always true
            if len(curr_prim.GetChildren()) == 0:
                value = curr_prim.GetAttribute(dataToFind).Get()
                # only add value to list if it's not 'None'
                if value != 'None':
                    if value == 'True' or value == 'Yes' or value == 'yes' or value == 'Y' or value == 'y':
                        tmp += [True]
                    elif value == 'False' or value == 'No' or value == 'no' or value == 'N' or value == 'n':
                        tmp += [False]
                    else:
                        # assumption is that data will either be boolean, float, or 'None'
                        tmp += [float(value)]
            else:
                tmp += LegendOverlay.findLayerData(curr_prim.GetChildren(), dataToFind)
        return tmp
    
    def findLayerData(children, dataToFind):
        """recursive helper function that returns a list of all the data in a layer, children is a list of all the children of the layer"""
        if len(children)==0:
            return []
        # determine if children[0] is a mesh or a layer, see assumption in findData()
        if len(children[0].GetChildren())==0:
            value = children[0].GetAttribute(dataToFind).Get()
            tmp = []
            if value != 'None':
                if value == 'True' or value == 'Yes' or value == 'yes' or value == 'Y' or value == 'y':
                    tmp = [True] 
                elif value == 'False' or value == 'No' or value == 'no' or value == 'N' or value == 'n':
                    tmp = [False] 
                else:
                    tmp = [float(value)]
            return tmp + LegendOverlay.findLayerData(children[1:], dataToFind)
        return LegendOverlay.findLayerData(children[0].GetChildren(), dataToFind) + LegendOverlay.findLayerData(children[1:], dataToFind)

    #----------------------------------#
    # Functions to make legend overlay #
    #----------------------------------#
    def make_legend_overlay(direction, legendColors, vp_window, isBoolData):
        """draws a legend with the colors of legendColors that overlays the viewport of viewport_window, and the placement is governed by direction"""
        with vp_window.frame:
            vp_window.frame.clear()
            # the scene_view height and width will be the viewport's heigt and width
            h=vp_window.height
            w=vp_window.width
            scene_view = sc.SceneView(
                aspect_ratio_policy=sc.AspectRatioPolicy.PRESERVE_ASPECT_FIT,
                height=h,
                width=w)
            scene_view.scene.clear()
            with scene_view.scene:
                # get the positions and sizes of each legend piece with this function
                trans, scale = LegendOverlay.make_overlay_points(direction, legendColors, vp_window, isBoolData)
                # legend will change whether data is boolean or float, boolean legend will have only first and last color while float will have full legend
                numColors = legendColors.len
                if isBoolData:
                    numColors = 2
                    # Draw the legend pieces
                for i in range(numColors):
                    legColor = (legendColors.color(i)[0], legendColors.color(i)[1], legendColors.color(i)[2], 1)
                    if isBoolData:
                        legColor = (legendColors.color(i*(legendColors.len-1))[0], legendColors.color(i*(legendColors.len-1))[1], legendColors.color(i*(legendColors.len-1))[2], 1)
                    # use translation to move rectangle to appropriate place on viewport
                    with sc.Transform(transform=sc.Matrix44.get_translation_matrix(trans[i][0], trans[i][1], trans[i][2])):
                        sc.Rectangle(color=legColor, height=scale[0], width=scale[1])
                # #Code for Testing coordinate system of sceneView in relation to viewport
                # aspect_ratio = w/h
                # height = 0.945
                # sc.Line([-1*aspect_ratio+0.01,-1*height,0], [aspect_ratio-0.05, 1, 0], color=(0,0,1,1), thickness=5)
                # sc.Line([-1*aspect_ratio+0.01,1,0], [aspect_ratio-0.05, -1*height, 0], color=(0,0,1,1), thickness=5)

                # sc.Line([0, -1*height, 0], [0, 1, 0], color=(1,0,0,1), thickness=5)
                # sc.Line([-1*aspect_ratio+0.01, 0, 0], [aspect_ratio-0.05, 0, 0], color=(1,0,0,1), thickness=5)

    def make_overlay_points(direction, legendColors, vp_window, isBoolData):
        """returns a 2D array trans for the positions of each legend piece on the viewport, 
        and returns a 2 element array scale of the height and width of each legend piece"""
        # For doing calculations
        h=vp_window.height
        w=vp_window.width
        aspect_ratio = w/h
        # change how many pieces to draw based on whether dat is boolean or not
        legColLen = legendColors.len
        if isBoolData:
            legColLen = 2
        margin = 0.1 #percentage offset from edges
        # Dict for the min, max values of the viewport frame, calculated with magic numbers found through testing
        coordSys = {"-x": -1*aspect_ratio+0.01, 
                    "+x": aspect_ratio-0.05, 
                    "-y": -0.945, 
                    "+y": 1}
        # return variables
        trans = []
        scale = []
        # Numbers for if legend will be on top or bottom
            # percent of total viewport height the legend will take up
            # the height of each legend piece that will also be the offset from the border
            # how wide each legend piece is, accounting for margins
        percH = 0.05
        offsetAndHeight = percH*(coordSys["+y"]-coordSys["-y"])
        stepSizeHoriz = (1-2*margin)*(coordSys["+x"]-coordSys["-x"])/legColLen
        # Numbers for if legend will be on left or right
        percW = 0.02
        offsetAndWidth = percW*(coordSys["+x"]-coordSys["-x"])
        stepSizeVert = (1-2*margin)*(coordSys["+y"]-coordSys["-y"])/legColLen
        # Calculate trans and scale 
        if(direction=='top'):
            for i in range(legColLen):
                # left edge plus margin for offset plus width of legend piece minus half of width of legend piece since this is the center of the legend piece
                trans.append([coordSys["-x"] + (margin)*(coordSys["+x"]-coordSys["-x"]) + stepSizeHoriz*(i+1) - stepSizeHoriz/2.0, 
                            coordSys["+y"] - offsetAndHeight,  # top edge minus height of legend piece which also acts as offset
                            0])
            scale = [offsetAndHeight, stepSizeHoriz]
        elif(direction=='bottom'):
            for i in range(legColLen):
                trans.append([coordSys["-x"] + (margin)*(coordSys["+x"]-coordSys["-x"]) + stepSizeHoriz*(i+1) - stepSizeHoriz/2.0, 
                            coordSys["-y"] + offsetAndHeight , 
                            0])
            scale = [offsetAndHeight, stepSizeHoriz]
        elif(direction=='left'):
            for i in range(legColLen):
                trans.append([coordSys["-x"] + offsetAndWidth, 
                            coordSys["-y"] + (margin)*(coordSys["+y"]-coordSys["-y"])+ stepSizeVert*(i+1)- stepSizeVert/2.0, 
                            0])
            scale = [stepSizeVert, offsetAndWidth]
        elif(direction=='right'):
            for i in range(legColLen):
                trans.append([coordSys["+x"] - offsetAndWidth, 
                            coordSys["-y"] + (margin)*(coordSys["+y"]-coordSys["-y"]) + stepSizeVert*(i+1)- stepSizeVert/2.0, 
                            0])
            scale = [stepSizeVert, offsetAndWidth]
        return trans, scale