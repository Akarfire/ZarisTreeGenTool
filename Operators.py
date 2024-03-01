import bpy
import os

from bpy.types import Operator


# Functions

# Checks for and appends all necessary assets to the file
def AppendAssets():

    CurrentDir = os.path.dirname(os.path.abspath(__file__))

    blendfile = CurrentDir + '/ZarisTreeGenTool_Assets.blend'

    GeometryNodes = ["Zaris_LeavesGenerator", "Zaris_Tree_LOD_Gen"]

    for GN in GeometryNodes:
        if not GN in bpy.data.node_groups :
            section   = 'NodeTree'
            object    = GN

            bpy.ops.wm.append(filepath=os.path.join(blendfile, section, object),
                            directory=os.path.join(blendfile, section),
                            filename=object)
    


# Actual Operators

class ZarisTreeGen_OT_CreateTreeBase(Operator):
    bl_idname = "object.create_tree_base"
    bl_label = "Create Tree Base"
    bl_description = "Creates a base for the tree trunk"

    @classmethod
    def poll(cls, context):
        if context.active_object == None:
            return True
        
        return context.active_object.mode == "OBJECT"

    def execute(self, context):

        # Check and append all necessary Assets before doing anything
        AppendAssets()

        # Parameteres
        DefaultTreeGenHeight = 2

        # Create tree base
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        CurrentObject = bpy.context.active_object
        CurrentObject.name = "TreeTrunk"

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.merge(type='CENTER')

        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, DefaultTreeGenHeight), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "alt_navigation":True, "use_automerge_and_split":False})

        bpy.ops.object.vertex_group_add()
        CurrentObject.vertex_groups[-1].name = "Trunk"


        bpy.ops.object.modifier_add(type='SKIN')
        bpy.context.object.modifiers["Skin"].use_smooth_shade = True

        bpy.ops.object.modifier_add(type='SUBSURF')

        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = 0.25

        return {'FINISHED'}



class ZarisTreeGen_OT_CreateLeavesBase(Operator):
    bl_idname = "object.create_leaves_base"
    bl_label = "Create Leaves Base"
    bl_description = "Creates a base for the tree leaves"

    @classmethod
    def poll(cls, context):
        if context.active_object == None:
            return True
        
        return context.active_object.mode == "OBJECT"

    def execute(self, context):

        # Check and append all necessary Assets before doing anything
        AppendAssets()

        bpy.ops.mesh.primitive_ico_sphere_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        CurrentObject = bpy.context.active_object
        CurrentObject.name = "TreeLeaves"

        Modifier = CurrentObject.modifiers.new("Leaves Generator", "NODES")
        ZarisLeavesGenerator = bpy.data.node_groups["Zaris_LeavesGenerator"]
        Modifier.node_group = ZarisLeavesGenerator

        return {'FINISHED'}
    


class ZarisTreeGen_OT_GenerateLODs(Operator):
    bl_idname = "object.generate_lods"
    bl_label = "Generate LODs"
    bl_description = "Generates LOD meshes for Zaris tree generation pipeline"

    @classmethod
    def poll(self, context):
        if context.active_object != None:

            FoundTrunkVG = False
            FoundCrownVG = False

            for vg in context.active_object.vertex_groups:
                FoundTrunkVG = FoundTrunkVG or vg.name == "Trunk"
                FoundCrownVG = FoundCrownVG or vg.name == "Crown"

                if FoundTrunkVG and FoundCrownVG: break

            return FoundTrunkVG and FoundCrownVG
        
        return False
    

    def AddLOD(self, OriginalName, LOD_ID, Spacing):

        Modded = False
        PreviousObject = None

        if OriginalName + "_LOD_" + str(LOD_ID) in bpy.data.objects:   
            bpy.ops.object.select_all(action='DESELECT')
            PreviousObject = bpy.data.objects[OriginalName + "_LOD_" + str(LOD_ID)]
            PreviousObject.select_set(True)
            PreviousObject.name = PreviousObject.name + "_temp"
            Modded = True

        TargetObjectName = OriginalName + "_LOD_" + str(LOD_ID - 1)
        if LOD_ID == 0:
            TargetObjectName = OriginalName


        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[TargetObjectName].select_set(True)
        
        bpy.ops.object.duplicate()
        bpy.ops.transform.translate(value=(Spacing, 0, 0))

        LOD = bpy.context.active_object
        LOD.name = OriginalName + "_LOD_" + str(LOD_ID)
        LOD.modifiers.clear()

        if PreviousObject != None:
            for mSrc in PreviousObject.modifiers:
                mDst = LOD.modifiers.get(mSrc.name, None)
                if not mDst:
                    mDst = LOD.modifiers.new(mSrc.name, mSrc.type)

                # collect names of writable properties
                properties = [p.identifier for p in mSrc.bl_rna.properties if not p.is_readonly]

                # copy those properties
                for prop in properties:
                    setattr(mDst, prop, getattr(mSrc, prop))

                if mSrc.type == "NODES":
                    for s in range(1, 100):
                        if ("Socket_" + str(s)) in LOD.modifiers[mSrc.name]:
                            LOD.modifiers[mSrc.name]["Socket_" + str(s)] = PreviousObject.modifiers[str(mSrc.name)]["Socket_" + str(s)]

                        if ("Socket_" + str(s) + '_attribute_name') in LOD.modifiers[mSrc.name]:
                            LOD.modifiers[mSrc.name]["Socket_" + str(s) + '_attribute_name'] = PreviousObject.modifiers[str(mSrc.name)]["Socket_" + str(s) + '_attribute_name']

                        if ("Socket_" + str(s) + '_use_attribute') in LOD.modifiers[mSrc.name]:
                            LOD.modifiers[mSrc.name]["Socket_" + str(s) + '_use_attribute'] = PreviousObject.modifiers[str(mSrc.name)]["Socket_" + str(s) + '_use_attribute']


        if OriginalName + "_LOD_" + str(LOD_ID) + "_temp" in bpy.data.objects:
            bpy.ops.object.select_all(action='DESELECT')  
            bpy.data.objects[OriginalName + "_LOD_" + str(LOD_ID) + "_temp"].select_set(True)
            bpy.ops.object.delete()

        return LOD, Modded




    def execute(self, context):

        AppendAssets()

        LOD_Number = 4
        LOD_Spacing = 6

        TargetObject = context.active_object
        OriginalName = TargetObject.name
        bpy.data.objects[TargetObject.name].select_set(True)

        LOD_0, LOD_0_Modded = self.AddLOD(OriginalName, 0, LOD_Spacing)

        for m in LOD_0.modifiers:
            bpy.ops.object.modifier_apply(modifier= m.name)
        
        for i in range(LOD_Number):

            LOD_Object, Modded = self.AddLOD(OriginalName, i + 1, LOD_Spacing)

            if not Modded:

                LOD_Object.modifiers.clear()
                Modifier = LOD_Object.modifiers.new("LOD Generator", "NODES")
                Zaris_Tree_LOD_Gen = bpy.data.node_groups["Zaris_Tree_LOD_Gen"]
                Modifier.node_group = Zaris_Tree_LOD_Gen

                bpy.ops.object.geometry_nodes_input_attribute_toggle(input_name="Socket_2", modifier_name="LOD Generator")
                bpy.ops.object.geometry_nodes_input_attribute_toggle(input_name="Socket_5", modifier_name="LOD Generator")
                LOD_Object.modifiers["LOD Generator"]["Socket_2_attribute_name"] = "Crown"   
                LOD_Object.modifiers["LOD Generator"]["Socket_5_attribute_name"] = "Trunk"


                LOD_Object.modifiers["LOD Generator"]["Socket_3"] = 1 / (1.25 * (i + 1))

            LOD_Object.data.update()


        return {'FINISHED'}
    