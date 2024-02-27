import bpy
from bpy.types import Panel

class ZarisTreeGen_PT_Panel (Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Zaris Tree Gen Tool"
    bl_category = "Zaris Tree Gen"

    def draw(self, context):

        layout = self.layout

        Row = layout.row()
        Column = Row.column()
        Column.operator("object.create_tree_base", text="Add Tree Base")
        Column.operator("object.create_leaves_base", text="Add Leaves Base")
        Column.operator("object.generate_lods", text="Generate LODs")

