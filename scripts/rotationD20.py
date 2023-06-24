import mathutils as mu

#vector maping of a d20
#todo: arange these guys in a map array

face_normals = [
    mu.Vector ((0.1876, -0.5774, -0.7947)),
    mu.Vector ((0.6071, 0.0000, -0.7947)),
    mu.Vector ((-0.4911, -0.3568, -0.7947)),
    mu.Vector ((-0.4911, 0.3568, -0.7947)),
    mu.Vector ((0.1876, 0.5774, -0.7947)),
    mu.Vector ((0.9822, 0.0000, -0.1876)),
    mu.Vector ((0.3035, -0.9342, -0.1876)),
    mu.Vector ((-0.7946, -0.5774, -0.1876)),
    mu.Vector ((-0.7946, 0.5774, -0.1876)),
    mu.Vector ((0.3035, 0.9342, -0.1876)),
    mu.Vector ((0.7946, -0.5774, 0.1876)),
    mu.Vector ((-0.3035, -0.9342, 0.1876)),
    mu.Vector ((-0.9822, 0.0000, 0.1876)),
    mu.Vector ((-0.3035, 0.9342, 0.1876)),
    mu.Vector ((0.7946, 0.5774, 0.1876)),
    mu.Vector ((0.4911, -0.3568, 0.7947)),
    mu.Vector ((-0.1876, -0.5774, 0.7947)),
    mu.Vector ((-0.6071, 0.0000, 0.7947)),
    mu.Vector ((-0.1876, 0.5774, 0.7947)),
    mu.Vector ((0.4911, 0.3568, 0.7947))
    ]
#rotates the given object so that the given normal is facing
#up
def face_up(obj,normal, up=mu.Vector((0,0,1))):
    identMat = mu.Matrix.Identity(4)

    theta = normal.angle(up)
    axis = normal.cross(up).normalized()
    mat = mu.Quaternion(axis,theta).to_matrix().to_4x4()

    obj.matrix_world = identMat@mat



if __name__ == '__main__':
    import bpy
    import random
    obj = bpy.context.active_object 
    face_up(obj,random.choice(face_normals))
    rotate_object(None,None)
