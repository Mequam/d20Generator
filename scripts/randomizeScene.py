"""
this file contains code used to randomize the 
scene containing the d20 for ai generation
"""
import os 
import bpy 
import random 
import time

#walks through the file structure and loads all of the fonts at the given path
#WARNING: this is a recursive walk, so gaurd your sym links and large folders
def load_fonts(path):
    for root,dirs,files in os.walk(path):
        for f in files:
            split_f = f.split('.')
            if  len(split_f) > 1 and (split_f [1] == 'ttf'):
                font = bpy.data.fonts.load(filepath=os.path.join(root,f))

#example accessing the fonts print([f for f in bpy.data.fonts])
#randomizes the font on the d20
def randomize_font():
    uv_texture_path = f"./uvTextureBuffer.png"
    normal_texture_path = f"./normalTextureBuffer.png"

    bpy.context.window.scene = bpy.data.scenes['geoNodeTexture']

    obj = bpy.context.scene.objects["Cube.001"]
    modifier = obj.modifiers[0]
    node_group = modifier.node_group
    node = node_group.nodes['String to Curves']
    node.font = random.choice(bpy.data.fonts)

    #render out an image without using the compistor for blur
    bpy.context.scene.use_nodes = False
    bpy.context.scene.render.filepath=uv_texture_path
    bpy.ops.render.render(write_still = True)

    #render out an image  using the compistor for blur
    bpy.context.scene.use_nodes = True
    bpy.context.scene.render.filepath=normal_texture_path
    bpy.ops.render.render(write_still = True)

    bpy.context.window.scene = bpy.data.scenes['d20']
   
    #load and set the uv texture for the dice to randomize the font
    #open the files that we outputed
    #bpy.ops.image.open(filepath="./",
    #    directory="./",
    #    files=[{"name":"bb.png",
    #    "name":"d20.png"}],
    #    relative_path=True 
    #    )    
    if 'uvTextureBuffer.png' in bpy.data.images:
        print('[*] removing previous texture image!')
        bpy.data.images.remove(bpy.data.images['uvTextureBuffer.png'])
    if 'normalTextureBuffer.png' in bpy.data.images:
        print('[*] removing previous normal image!')
        bpy.data.images.remove(bpy.data.images['normalTextureBuffer.png'])

    print("after open")
    uv_texture = bpy.data.images.load(uv_texture_path,check_existing=True)
    #bpy.data.images["uvTexture.png"]
    normal_texture = bpy.data.images.load(normal_texture_path,check_existing=True)
    #bpy.data.images["normalTexture.png"]

    #tell the material of the dice to use those images

    dice = bpy.context.scene.objects["rotater"]
    shader_material = dice.material_slots[0].material 

    shader_material.node_tree.nodes['Image Texture'].image = uv_texture
    shader_material.node_tree.nodes['Image Texture.003'].image = normal_texture 



#use a main function,
#like some c++ NERD
def main():
    randomize_font()


if __name__ == '__main__':
    main()
