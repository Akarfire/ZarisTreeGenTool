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

Classes = (ZarisTreeGen_PT_Panel, ZarisTreeGen_OT_CreateTreeBase, ZarisTreeGen_OT_CreateLeavesBase)

def register():
    for c in Classes:
        bpy.utils.register_class(c)

def unregister():
    for c in Classes:
        bpy.utils.unregister_class(c)


CurrentDir = os.path.dirname(os.path.abspath(__file__))

blendfile = CurrentDir + '/ZarisTreeGenTool_Assets.blend'
section   = 'NodeTree'
object    = 'Zaris_LeavesGenerator'


blendfile = 'D:/3D_Models/Blender/Scripts/ZarisTreeGenTool/ZarisTreeGenTool_Assets.blend'
# Filepath  = blendfile + section + object
# Directory = blendfile + section
# Filename  = object

bpy.ops.wm.append(filepath=os.path.join(blendfile, section, object),
                  directory=os.path.join(blendfile, section),
                  filename=object)