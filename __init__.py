# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "ZarisTreeGenTool",
    "author" : "AkarFire aka KScarlet",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy
import os

from . Panels import ZarisTreeGen_PT_Panel
from . Operators import ZarisTreeGen_OT_CreateTreeBase
from . Operators import ZarisTreeGen_OT_CreateLeavesBase
# from bpy.utils import resource_path
# from pathlib import Path


# filepath = os.path.join(os.path.dirname(
# os.path.abspath(__file__)), self.blend + ".blend")
        
# with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
#     data_to.node_groups = [
#         name for name in data_from.node_groups]


Classes = (ZarisTreeGen_PT_Panel, ZarisTreeGen_OT_CreateTreeBase, ZarisTreeGen_OT_CreateLeavesBase)

def register():
    for c in Classes:
        bpy.utils.register_class(c)

def unregister():
    for c in Classes:
        bpy.utils.unregister_class(c)
