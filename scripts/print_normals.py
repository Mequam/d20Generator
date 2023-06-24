"""
prints the normals of the faces of the currently selected
object in blender
"""
import bpy
f = open('output.txt','w')

obj = bpy.context.active_object
for p in obj.data.polygons:
    f.write(str(p.normal))
    print(p.normal) #face normal
f.close()
#rotates the given icosphere to the given d20 number face
#with a given normal mapping
#def rotate_face():
