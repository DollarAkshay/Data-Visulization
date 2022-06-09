import bpy
import math
import numpy as np
import random


# A function to clear the scene
def clear_scene():
    # Clear All Objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True)

    # Clear all collections
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)

# Create a new collection and link it


def create_collection(name, color=None):

    color = f'COLOR_{random.randint(1, 8):02d}' if color is None else color
    new_collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(new_collection)
    bpy.data.collections[name].color_tag = color


# Reset the collection to Scene Collection
def reset_collection():
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection


# Set the active collection to the new collection
def switch_to_collection(name):
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[name]


# Main Code
clear_scene()


# Setup Lighting
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.85, 0.955, 1, 1)
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.2
bpy.context.scene.cycles.use_fast_gi = True

# Setup Scene
bpy.ops.mesh.primitive_plane_add(size=10000, location=(0, 0, 0))

create_collection('Cubes', color='COLOR_02')
switch_to_collection('Cubes')

# Add multiple Cubes
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5, 0.5, 0.5))
cube = bpy.context.selected_objects[0]
dimensions = [16, 16, 0]  # Rows, Columns, Levels

for i in range(3):
    mod = cube.modifiers.new('Array', 'ARRAY')
    mod.relative_offset_displace[0] = 0
    mod.relative_offset_displace[i] = 1.5
    mod.count = dimensions[i]
    bpy.ops.object.modifier_apply(modifier='Array')

bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

reset_collection()


# Create light datablock, set attributes
light_data = bpy.data.lights.new(name='Sunlight', type='SUN')
light_data.energy = 8
light_data.color = (0.78, 0.868, 1)
light_data.angle = 135 * math.pi / 180

# Create new object with our light datablock
light_object = bpy.data.objects.new(name='Sunlight', object_data=light_data)
bpy.context.collection.objects.link(light_object)
