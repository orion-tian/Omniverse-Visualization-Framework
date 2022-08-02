import omni.ext
import omni.ui as ui
import omni.kit.commands
import omni.usd
from pxr import UsdShade, Gf, Sdf
import omni.kit.viewport
from omni.ui import scene as sc
from omni.ui import color as cl


class Legend(omni.ext.IExt):

    boundingBox = {}

    def makeLegendParam(data, legendColors):
        legendParam = {}
        min = data[0]
        max = data[0]
        for d in data:
            if d<min:
                min = d
            if d>max:
                max = d
        legendParam.update({"min" : min})
        legendParam.update({"max" : max})
        legendParam.update({"steps" : len(legendColors)})
        legendParam.update({"step size" : (max+1-min)/len(legendColors)})

        return legendParam

    def calcBoundingBox(prim):
        boundingBox = {}
        scaleFactor = 50 # Plane are 100x100 units so need half to get from center to edge
        center = [prim.GetAttribute("xformOp:translate").Get()[0], prim.GetAttribute("xformOp:translate").Get()[1], prim.GetAttribute("xformOp:translate").Get()[2]]
        scaling = [prim.GetAttribute("xformOp:scale").Get()[0], prim.GetAttribute("xformOp:scale").Get()[1], prim.GetAttribute("xformOp:scale").Get()[2]]
        boundingBox.update({"-x": center[0]-scaleFactor*scaling[0]})
        boundingBox.update({"+x": center[0]+scaleFactor*scaling[0]})
        boundingBox.update({"-z": center[2]-scaleFactor*scaling[2]})
        boundingBox.update({"+z": center[2]+scaleFactor*scaling[2]})

        return boundingBox

    def calcEntireBoundingBox(selected_prims):
        omni.usd.get_context().get_selection().set_selected_prim_paths(selected_prims, False)
        sel_prims = omni.usd.get_context().get_selection().get_selected_prim_paths()
        curr_prim = omni.usd.get_context().get_stage().GetPrimAtPath(sel_prims[0])
        firstChild = curr_prim.GetChildren()[0]
        Legend.boundingBox = Legend.calcBoundingBox(firstChild)
        tmp = {}
        for s in sel_prims:
            curr_prim = omni.usd.get_context().get_stage().GetPrimAtPath(s)
            children = curr_prim.GetChildren()
            for c in children:
                tmp = Legend.calcBoundingBox(c)
                if(tmp.get("-x")<Legend.boundingBox.get("-x")):
                    Legend.boundingBox.update({"-x": tmp.get("-x")})
                if(tmp.get("+x")>Legend.boundingBox.get("+x")):
                    Legend.boundingBox.update({"+x": tmp.get("+x")})
                if(tmp.get("-z")<Legend.boundingBox.get("-z")):
                    Legend.boundingBox.update({"-z": tmp.get("-z")})
                if(tmp.get("+z")>Legend.boundingBox.get("+z")):
                    Legend.boundingBox.update({"+z": tmp.get("+z")})
    
    def make_Vec(direction, legendColors, selected_prims):
        transVec = []
        scaleVec = []
        Legend.calcEntireBoundingBox(selected_prims)
        legColLen = len(legendColors)
        lengthWidthRatio = 15
        planeSize = 100 # Default Plane is 100x100 units

        if direction == "+z":
            stepSize = (Legend.boundingBox["+x"]-Legend.boundingBox["-x"])/legColLen
            scaleLengthactor = stepSize/planeSize
            scaleWidthFactor = (Legend.boundingBox["+x"]-Legend.boundingBox["-x"])/lengthWidthRatio/planeSize
            offset = (Legend.boundingBox["+x"]-Legend.boundingBox["-x"])/lengthWidthRatio
            for i in range(legColLen):
                transVec.append(Gf.Vec3f(Legend.boundingBox["-x"] + (stepSize*(i+1) - stepSize/2.0), 0.0, Legend.boundingBox["+z"] + offset))
                scaleVec.append(Gf.Vec3f(scaleLengthactor, 1.0, scaleWidthFactor))
        elif direction == "-z":
            stepSize = (Legend.boundingBox["+x"]-Legend.boundingBox["-x"])/legColLen
            scaleLengthactor = stepSize/planeSize 
            scaleWidthFactor = (Legend.boundingBox["+x"]-Legend.boundingBox["-x"])/lengthWidthRatio/planeSize
            offset = (Legend.boundingBox["+x"]-Legend.boundingBox["-x"])/lengthWidthRatio
            for i in range(legColLen):
                transVec.append(Gf.Vec3f(Legend.boundingBox["+x"] - (stepSize*(i+1) - stepSize/2.0), 0.0, Legend.boundingBox["-z"] - offset))
                scaleVec.append(Gf.Vec3f(scaleLengthactor, 1.0, scaleWidthFactor))
        elif direction == "+x":
            stepSize = (Legend.boundingBox["+z"]-Legend.boundingBox["-z"])/legColLen
            scaleLengthactor = stepSize/planeSize 
            scaleWidthFactor = (Legend.boundingBox["+z"]-Legend.boundingBox["-z"])/lengthWidthRatio/planeSize
            offset = (Legend.boundingBox["+z"]-Legend.boundingBox["-z"])/lengthWidthRatio
            for i in range(legColLen):
                transVec.append(Gf.Vec3f(Legend.boundingBox["+x"] + offset, 0.0, Legend.boundingBox["+z"] - (stepSize*(i+1) - stepSize/2.0)))
                scaleVec.append(Gf.Vec3f(scaleWidthFactor, 1.0, scaleLengthactor))
        else:
            stepSize = (Legend.boundingBox["+z"]-Legend.boundingBox["-z"])/legColLen
            scaleLengthactor = stepSize/planeSize 
            scaleWidthFactor = (Legend.boundingBox["+z"]-Legend.boundingBox["-z"])/lengthWidthRatio/planeSize
            offset = (Legend.boundingBox["+z"]-Legend.boundingBox["-z"])/lengthWidthRatio
            for i in range(legColLen):
                transVec.append(Gf.Vec3f(Legend.boundingBox["-x"] - offset, 0.0, Legend.boundingBox["-z"] + (stepSize*(i+1) - stepSize/2.0)))
                scaleVec.append(Gf.Vec3f(scaleWidthFactor, 1.0, scaleLengthactor))
        return transVec, scaleVec

    def make_legend(selected_prims, direction, legendColors):
        stage = omni.usd.get_context().get_stage()
        legendPrim = stage.DefinePrim('/World/Energy_Results/Legend', 'Scope')
        legendMatPrim = stage.DefinePrim('/World/Energy_Results/Legend/Materials', 'Scope')

        transVec, scaleVec = Legend.make_Vec(direction, legendColors, selected_prims)
        new_mtl_created_list = []

        for i in range(len(legendColors)):
            result, path = omni.kit.commands.execute('CreateMeshPrimWithDefaultXform', prim_type='Plane')
            omni.kit.commands.execute('ChangeProperty',
                prop_path=path + '.xformOp:translate',
                value=transVec[i],
                prev=None)
            omni.kit.commands.execute('ChangeProperty',
                prop_path=path + '.xformOp:scale',
                value=scaleVec[i],
                prev=None)
            
            omni.usd.get_context().get_selection().set_selected_prim_paths([path], False)
            #create and bind material
            omni.kit.commands.execute(
                "CreateAndBindMdlMaterialFromLibrary",
                mdl_name="OmniPBR.mdl",
                mtl_name="OmniPBR",
                mtl_created_list=new_mtl_created_list,
                bind_selected_prims=True)
            mtl = new_mtl_created_list[len(new_mtl_created_list)-1]
            stage = omni.usd.get_context().get_stage()
            mtl_prim = stage.GetPrimAtPath(mtl)
            rough = 1.0
            # Set material inputs, these can be determined by looking at the .mdl file
            # or by selecting the Shader attached to the Material in the stage window and looking at the details panel
            omni.usd.create_material_input(mtl_prim, "diffuse_tint", legendColors[i], Sdf.ValueTypeNames.Color3f)
            omni.usd.create_material_input(mtl_prim, "reflection_roughness_constant", rough, Sdf.ValueTypeNames.Float)
            # move material and plane into a scope for convenience
            omni.kit.commands.execute('MovePrim',
                                    path_from=mtl,
                                    path_to=legendMatPrim.GetPath().pathString + '/legendColor')
            omni.kit.commands.execute('MovePrim',
                                    path_from=path,
                                    path_to=legendPrim.GetPath().pathString + '/PlaneLegend')