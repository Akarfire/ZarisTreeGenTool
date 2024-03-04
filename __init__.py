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

from . Panels import *
from . Operators import *

Classes = (ZarisTreeGen_PT_CreateTree, ZarisTreeGen_PT_GenerateLODs, ZarisTreeGen_OT_CreateTreeBase, ZarisTreeGen_OT_CreateLeavesBase, ZarisTreeGen_OT_GenerateLODs, ZarisTreeGen_OT_AddTrunkGeometry,
           ZarisTreeGen_OT_LeavesShading, ZarisTreeGen_OT_PackTree, ZarisTreeGen_OT_PackLODs, ZarisTreeGen_OT_UnpackLODs)

def register():
    for c in Classes:
        bpy.utils.register_class(c)

def unregister():
    for c in Classes:
        bpy.utils.unregister_class(c)


