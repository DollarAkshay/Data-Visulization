import bmesh
import bpy
import math
import numpy as np
from perlin_noise import PerlinNoise
import random
import time

C = bpy.context
D = bpy.data
noise = PerlinNoise(8, seed=time.time())

# A function to clear the scene


def clear_scene():
    # Switch to object mode if in edit mode
    if C.object and C.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Delete all materials
    for material in D.materials:
        D.materials.remove(material)

    # Clear All Objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True)

    # Clear all collections
    for collection in D.collections:
        D.collections.remove(collection)


# Create a new collection and link it
def create_collection(name, color=None):

    color = f'COLOR_{random.randint(1, 8):02d}' if color is None else color
    new_collection = D.collections.new(name)
    C.scene.collection.children.link(new_collection)
    D.collections[name].color_tag = color


# Reset the collection to Scene Collection
def reset_collection():
    C.view_layer.active_layer_collection = C.view_layer.layer_collection


# Set the active collection to the new collection
def switch_to_collection(name):
    C.view_layer.active_layer_collection = C.view_layer.layer_collection.children[name]


# Function to setup Lighting
def setup_lighting():
    D.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.85, 0.955, 1, 1)
    D.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.2
    C.scene.cycles.use_fast_gi = True
    C.scene.world.light_settings.ao_factor = 1
    C.scene.world.light_settings.distance = 5

    # Create light datablock, set attributes
    light_data = D.lights.new(name='Sunlight', type='SUN')
    light_data.energy = 8
    light_data.color = (0.78, 0.868, 1)
    light_data.angle = 135 * math.pi / 180

    # Create new object with our light datablock
    light_object = D.objects.new(name='Sunlight', object_data=light_data)
    C.collection.objects.link(light_object)


# Function to setup Scene and cameras
def setup_scene():
    bpy.ops.mesh.primitive_plane_add(size=10000, location=(0, 0, -1))
    bpy.ops.object.camera_add(location=(50, 50, 200), rotation=(0, 0, 0))


# Main Code
clear_scene()
setup_scene()
setup_lighting()


# Build up the Mesh
start_time = time.time()
grid_mesh = bpy.data.meshes.new('Cube Grid')
grid_size = [100, 100, 25]

cube_size = 0.9
verts = []
faces = []


for x in range(grid_size[0]):
    for y in range(grid_size[1]):
        h = round((noise([x / grid_size[0], y / grid_size[1]]) + 1) * grid_size[2] / 2)
        for z in range(h - 4, h):

            # Add the vertices of a cube from front to back
            verts.append([-cube_size / 2 + x, +cube_size / 2 + y, +cube_size / 2 + z])
            verts.append([+cube_size / 2 + x, +cube_size / 2 + y, +cube_size / 2 + z])
            verts.append([-cube_size / 2 + x, -cube_size / 2 + y, +cube_size / 2 + z])
            verts.append([+cube_size / 2 + x, -cube_size / 2 + y, +cube_size / 2 + z])
            verts.append([-cube_size / 2 + x, +cube_size / 2 + y, -cube_size / 2 + z])
            verts.append([+cube_size / 2 + x, +cube_size / 2 + y, -cube_size / 2 + z])
            verts.append([-cube_size / 2 + x, -cube_size / 2 + y, -cube_size / 2 + z])
            verts.append([+cube_size / 2 + x, -cube_size / 2 + y, -cube_size / 2 + z])

            # Add the faces of a cube.
            vertOffset = len(verts) - 8
            faces.append([vertOffset + 0, vertOffset + 1, vertOffset + 3, vertOffset + 2])  # Front
            faces.append([vertOffset + 5, vertOffset + 4, vertOffset + 6, vertOffset + 7])  # Back
            faces.append([vertOffset + 4, vertOffset + 0, vertOffset + 2, vertOffset + 6])  # Left
            faces.append([vertOffset + 1, vertOffset + 5, vertOffset + 7, vertOffset + 3])  # Right
            faces.append([vertOffset + 4, vertOffset + 5, vertOffset + 1, vertOffset + 0])  # Top
            faces.append([vertOffset + 2, vertOffset + 3, vertOffset + 7, vertOffset + 6])  # Bottom

grid_mesh.from_pydata(verts, [], faces)
grid_mesh.update()

# Create the new object
cube_object = D.objects.new(name='Cube Grid', object_data=grid_mesh)
C.collection.objects.link(cube_object)

# Create a simple black diffuse principled BSDF material
material_1 = D.materials.new('Diffuse 1')
material_1.use_nodes = True
bsdf = material_1.node_tree.nodes["Principled BSDF"].inputs
bsdf['Diffuse Color'].default_value = (0.0, 0.0, 0.0, 1.0)
bsdf['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)
bsdf['Metallic'].default_value = 0.0
bsdf['Roughness'].default_value = 0.0
bsdf['Specular'].default_value = 0.0
bsdf['Specular Tint'].default_value = 0.0
bsdf['Subsurface'].default_value = 0.0
bsdf['Subsurface Color'].default_value = (0.0, 0.0, 0.0, 1.0)
bsdf['Metallic'].default_value = 0.0

# Create a simple orange emission material
material_2 = D.materials.new('Emission 1')
material_2.use_nodes = True
bsdf = material_2.node_tree.nodes["Principled BSDF"].inputs
bsdf['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)
bsdf['Emission Color'].default_value = (0.8, 0.5, 0.0, 1.0)
bsdf['Emission'].default_value = 1.0

# Create a simple redish-purple emission material
material_3 = D.materials.new('Emission 2')
material_3.use_nodes = True
bsdf = material_3.node_tree.nodes["Principled BSDF"].inputs
bsdf['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)
bsdf['Emission Color'].default_value = (0.5, 0.0, 0.5, 1.0)
bsdf['Emission'].default_value = 1.0

cube_object.data.materials.append(material_1)

# modifier = cube_object.modifiers.new(name="BEVEL", type='BEVEL')
# modifier.width = 0.05
# modifier.segments = 4

print(f'Mesh creation time: {time.time() - start_time:.2f} sec')

bpy.ops.object.select_all(action='DESELECT')
