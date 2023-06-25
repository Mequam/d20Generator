"""
this file contains code used to randomize the 
scene containing the d20 for ai generation
"""
import os 
import bpy 
import random

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
    bpy.context.window.scene = bpy.data.scenes['geoNodeTexture']

    obj = bpy.context.scene.objects["Cube.001"]
    modifier = obj.modifiers[0]
    node_group = modifier.node_group
    node = node_group.nodes['String to Curves']
    node.font = random.choice(bpy.data.fonts)

    #render out an image without using the compistor for blur
    bpy.context.scene.use_nodes = False
    bpy.context.scene.render.filepath="./test_d20_texture.png"
    bpy.ops.render.render(write_still = True)

    #render out an image  using the compistor for blur
    bpy.context.scene.use_nodes = True
    bpy.context.scene.render.filepath="./bump_blur.png"
    bpy.ops.render.render(write_still = True)

    bpy.context.window.scene = bpy.data.scenes['d20']
   
    



randomize_font()
