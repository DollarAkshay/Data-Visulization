import bpy
import math
import numpy as np


# A function to clear the scene
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True)


# Main Code
clear_scene()

# Add multiple Cubes
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5, 0.5, 0.5))
cube = bpy.context.selected_objects[0]
dimensions = [10, 10, 0]  # Rows, Columns, Levels

for i in range(3):
    mod = cube.modifiers.new('Array', 'ARRAY')
    mod.relative_offset_displace[0] = 0
    mod.relative_offset_displace[i] = 1.1
    mod.count = dimensions[i]
    bpy.ops.object.modifier_apply(modifier='Array')

bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
