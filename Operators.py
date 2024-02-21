import bpy

from bpy.types import Operator


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

        bpy.ops.mesh.primitive_ico_sphere_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        CurrentObject = bpy.context.active_object
        CurrentObject.name = "TreeLeaves"

        # modifier = CurrentObject.modifiers.new("Leaves Generator", "NODES")
        # ZarisLeavesGenerator = bpy.data.node_groups["ZarisLeavesGenerator"]
        # modifier.node_group = ZarisLeavesGenerator


        return {'FINISHED'}
    


