"""
this file contains code used to randomize the 
scene containing the d20 for ai generation
"""
import os 

import random 
import time 
import math

import bpy 
from mathutils import Euler 
from mathutils import Color 

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
   
    if 'uvTextureBuffer.png' in bpy.data.images:
        #print('[*] removing previous texture image!')
        bpy.data.images.remove(bpy.data.images['uvTextureBuffer.png'])
    if 'normalTextureBuffer.png' in bpy.data.images:
        #print('[*] removing previous normal image!')
        bpy.data.images.remove(bpy.data.images['normalTextureBuffer.png'])

    #print("after open")
    uv_texture = bpy.data.images.load(uv_texture_path,check_existing=True)
    #bpy.data.images["uvTexture.png"]
    normal_texture = bpy.data.images.load(normal_texture_path,check_existing=True)
    #bpy.data.images["normalTexture.png"]

    #tell the material of the dice to use those images

    dice = bpy.context.scene.objects["rotater"]
    shader_material = dice.material_slots[0].material 

    shader_material.node_tree.nodes['Image Texture'].image = uv_texture
    shader_material.node_tree.nodes['Image Texture.003'].image = normal_texture 

def generateBiasUnif(start,end,bias=1):
    ret_val = 0
    for i in range(bias):
        ret_val += random.uniform(start,end)
    #print(f"returning {ret_val}" )
    return ret_val / bias

#randomizes the rotation and layout of the camera,
#while still having it point twoards the dice
def randomize_rotation(name,bias=(2,2,1),domain=((-math.pi/4,math.pi/4),(-math.pi/4,math.pi/4),(0,2*math.pi))):
    obj = bpy.context.scene.objects[name]
    obj.rotation_euler = Euler((
                                generateBiasUnif(domain[0][0],domain[0][1],bias[0]),
                                generateBiasUnif(domain[1][0],domain[1][1],bias[1]),
                                generateBiasUnif(domain[2][0],domain[2][1],bias[2])),'XYZ')
def get_random_color():
    return (random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),1.0)

def square_color_distance(c1,c2):
    return (Color((c1[0],c1[1],c1[2])).h - Color((c2[0],c2[1],c2[2])).h)**2
        
#randomizes the sader effects of the dice
#to several preset and random vlues
def generate_readable_color(backgrounds,threshold = 0.5):
    ret_val = get_random_color()
    s = sum([square_color_distance(b,ret_val) for b in backgrounds])/len(backgrounds)
    #print(s)
    while  s < 0.2:
        #print(s)
        ret_val = get_random_color()
        s = sum([square_color_distance(b,ret_val) for b in backgrounds])/len(backgrounds)
    return ret_val

def randomize_dice_shader():
    obj = bpy.context.scene.objects["rotater"]
    
    #randomize the colors

    mat = obj.material_slots[0].material 
    colormap = mat.node_tree.nodes['ColorGroup']
   
    background_color = get_random_color()
    splash_color = get_random_color()
    mat.node_tree.nodes['MainColor'].outputs['Color'].default_value = background_color
    mat.node_tree.nodes['SplashColor'].outputs['Color'].default_value = splash_color if random.uniform(0,1) < .5 else background_color
    mat.node_tree.nodes['TextColor'].outputs['Color'].default_value = generate_readable_color([background_color,splash_color])


    

    #randomize the belile amount
    if random.uniform(0,1) < .1:
        obj.modifiers["Bevel"].width = 0 #make sure that at least SOME of them have no bevling
    else:
        obj.modifiers["Bevel"].width = random.uniform(0,0.1)

    #how see through are we?
    x = random.uniform(0,1)
    if  x < .25: #make sure that we have at least SOME perfect glass dice
        mat.node_tree.nodes['Transmision Range'].inputs['To Min'].default_value = 1
        mat.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 0.0
        mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = random.uniform(0,0.5)
        print("glass dice")
    elif x < .5: #metalic dice
        mat.node_tree.nodes['Transmision Range'].inputs['To Min'].default_value = 0
        mat.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 1.0
        mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = random.uniform(0,1)
        print("metal dice")
    else: #eh, let rnjesus decide
        mat.node_tree.nodes['Transmision Range'].inputs['To Min'].default_value = random.uniform(0,1)
        mat.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = random.uniform(0,1)
        mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = random.uniform(0,1)
        print("misc dice")

def randomize_floor_shader():
    obj = bpy.context.scene.objects["floor"]
    mat = obj.material_slots[0].material 
    elements = mat.node_tree.nodes['Color Ramp'].color_ramp.elements 
    stepSize = 1/len(elements)
    for i in range(len(elements)):
        elements[i].color = get_random_color()
        x = generateBiasUnif(0,stepSize,2)+stepSize*i
        elements[i].position = x if x <= 1.0 else 1.0


    vornoliTexture = mat.node_tree.nodes['RandText']
    vornoliTexture.inputs['Randomness'].default_value = random.uniform(0,1)
    vornoliTexture.inputs['Scale'].default_value = random.uniform(0,50)

    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = random.uniform(0,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = random.uniform(0.5,1)


#use a main function,
#like some c++ NERD
def main():
    randomize_font()
    randomize_rotation("Camera")
    randomize_rotation("Light",(4,4,1))
    randomize_dice_shader()
    randomize_floor_shader()

if __name__ == '__main__':
    main()
