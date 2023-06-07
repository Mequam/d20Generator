"""The uv coordinates are stored in 'loops':

You set ob.data.uv_layers.active.data[loop_index].uv = (0.5, 0.5)

You can see how loops work here:
"""

import bpy 
import bmesh
from mathutils import Vector

ob = bpy.context.object 

 # Create an empty mesh and the object.
mesh = bpy.data.meshes.new('d20_uv_mesh')
output_object = bpy.data.objects.new("d20_uv",mesh)

# Add the object into the scene.
bpy.data.collections['uv_choord_verts'].objects.link(output_object)

# Select the newly created object
bpy.context.view_layer.objects.active = output_object
output_object.select_set(True)

# Construct the bmesh that we fill with points
bm = bmesh.new()


#TODO: this needs 
#to be an array lookup for the mapping on a d20
def index_map_d20(idx):
    return idx + 1


# Loops per face
for face in ob.data.polygons:
    center = Vector((0,0))
    for loop_idx in face.loop_indices:
        uv_coords = ob.data.uv_layers.active.data[loop_idx].uv 
        center += uv_coords
        #print("face idx: %i, uvs: %f, %f" % (face.index, uv_coords.x, uv_coords.y))
    center /= 3
    print("face idx: %i , center: %f, %f" % (face.index,center.x,center.y))
    bm.verts.new((center.x,center.y,index_map_d20(face.index)))

#store our bmesh into the mesh object
bm.to_mesh(mesh)
bm.free() #remove the bmesh from python memory
# Or just cycle all loops
#for loop in ob.data.loops :
#    uv_coords = ob.data.uv_layers.active.data[loop.index].uv
#    print(uv_coords)


# from https://docs.blender.org/api/current/bpy.types.Mesh.html#mesh-id

#me = bpy.context.object.data
#uv_layer = me.uv_layers.active.data
#
#for poly in me.polygons:
#    print("Polygon index: %d, length: %d" % (poly.index, poly.loop_total))
#
#    # range is used here to show how the polygons reference loops,
#    # for convenience 'poly.loop_indices' can be used instead.
#    for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
#        print("    Vertex: %d" % me.loops[loop_index].vertex_index)
#        print("    UV: %r" % uv_layer[loop_index].uv)
#
