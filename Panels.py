import bpy
from bpy.types import Panel

class ZarisTreeGen_PT_CreateTree (Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Tree Generation"
    bl_category = "Zaris Tree Gen"

    def draw(self, context):

        layout = self.layout

        Row = layout.row()
        Column = Row.column()
        Column.operator("object.create_tree_base", text="Add Tree Base")
        Column.operator("object.add_trunk_geometry", text="Add Trunk Geometry")
        Column.operator("object.create_leaves_base", text="Add Leaves Base")
        Column.operator("object.leaves_shading", text="Set Up Leaves Shading")
        Column.operator("object.pack_tree", text="Pack Tree")



class ZarisTreeGen_PT_GenerateLODs (Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "LOD Generation"
    bl_category = "Zaris Tree Gen"

    def draw(self, context):

        layout = self.layout

        Row = layout.row()
        Column = Row.column()
        Column.operator("object.generate_lods", text="Generate LODs")
        Column.operator("object.pack_lods", text="Pack LODs")
        Column.operator("object.unpack_lods", text="Unpack LODs")
