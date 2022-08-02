import omni.usd

class MeshNames:

    def findNames():
        """returns a list of the names of the meshes in the selected prims,
        assumption: a prim with children is a scope/xform and not a mesh, which isn't always true,
        warning: best to collapse all layers to avoid duplicates"""
        tmp = []
        context = omni.usd.get_context()
        selected_prims = context.get_selection().get_selected_prim_paths()
        for s in selected_prims:
            curr_prim = context.get_stage().GetPrimAtPath(s)
            # determine if s is a mesh or layer
            if len(curr_prim.GetChildren()) == 0:
                tmp += [curr_prim.GetName()]
            else:
                tmp += MeshNames.findLayerNames(curr_prim.GetChildren())
        return tmp

    def findLayerNames(children):
        """recursive helper function that returns a list of the mesh names for a layer"""
        if len(children)==0:
            return []
        # determine if children[0] is a mesh or a layer
        if len(children[0].GetChildren())==0:
            return [children[0].GetName()] + MeshNames.findLayerNames(children[1:])
        return MeshNames.findLayerNames(children[0].GetChildren()) + MeshNames.findLayerNames(children[1:])