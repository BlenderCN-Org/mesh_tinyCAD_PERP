"""
2016 Dealga McArdle | zeffii@hotmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""  


bl_info = {
    "name": "PERP addon for tinycad",
    "description": "this tinycad add-on makes a perpendicular edge between active vertex and 2 selected vertices",
    "author": "Dealga McArdle",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "category": "Mesh"
}


import bpy
import bmesh
import mathutils

ipl = mathutils.geometry.intersect_point_line


def perp_make():

    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    active_vert = bm.select_history.active
    selected_verts = [v for v in bm.verts if v.select and not v.hide]

    if len(selected_verts) == 3:
        other_verts = set(selected_verts).symmetric_difference({active_vert})
        pt = active_vert.co
        line_p1 = other_verts.pop().co
        line_p2 = other_verts.pop().co
        new_vert, factor = ipl(pt, line_p1, line_p2)
        vec1 = bm.verts.new(new_vert)
        bm.verts.ensure_lookup_table()
        bm.edges.new((vec1, active_vert))

    bmesh.update_edit_mesh(me, True)
    

class TCPerpEdge(bpy.types.Operator):
    bl_idname = "tinycad.perp_edge"
    bl_label = "PERP | Perpendicular Edge creation"
    bl_description = "Extends an edge from active vertex to perpendicular of 2 selected vertices"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if not (tuple(context.tool_settings.mesh_select_mode[:]) == (True, False, False)):
            return
        
        # is edit mode, is vertex select mode only. 
        ob = context.active_object
        return all([bool(ob), ob.type == 'MESH', ob.mode == 'EDIT'])

    def execute(self, context):
        perp_make()
        return {"CANCELLED"}


def menu_func(self, context):
    operator = self.layout.operator
    operator("tinycad.perp_edge")


def register():
    bpy.utils.register_module(__name__)
    try:
        bpy.types.VIEW3D_MT_edit_mesh_tinycad.append(menu_func)
    except:
        print('mesh_tinyCAD menu not found, cannot add')

def unregister():
    bpy.utils.unregister_module(__name__)
    try:
        bpy.types.VIEW3D_MT_edit_mesh_tinycad.remove(menu_func)
    except:
        ...