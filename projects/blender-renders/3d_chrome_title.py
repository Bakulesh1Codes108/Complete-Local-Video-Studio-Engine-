
import bpy
import math

# Clear existing objects
bpy.ops.wm.read_factory_settings(use_empty=True)

# Scene setup
scene = bpy.context.scene
scene.render.engine = 'CYCLES' if bpy.context.preferences.addons.get('cycles') else 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 90

# Camera
cam_data = bpy.data.cameras.new("StudioCamera")
cam_obj = bpy.data.objects.new("StudioCamera", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Camera Animation (Crane Down & Dolly In)
cam_obj.location = (0, -6.5, 3.2)
cam_obj.rotation_euler = (math.radians(65), 0, 0)
cam_obj.keyframe_insert(data_path="location", frame=1)
cam_obj.location = (0, -4.8, 1.2)
cam_obj.rotation_euler = (math.radians(80), 0, 0)
cam_obj.keyframe_insert(data_path="location", frame=90)

# 3D Extruded Text
font_curve = bpy.data.curves.new(type="FONT", name="TitleCurve")
font_curve.body = "QUANTUM AWAKENING"
font_curve.extrude = 0.15
font_curve.bevel_depth = 0.03
font_curve.align_x = 'CENTER'
font_curve.align_y = 'CENTER'

text_obj = bpy.data.objects.new("TitleObject", font_curve)
bpy.context.collection.objects.link(text_obj)
text_obj.location = (0, 0, 0)

# Metallic Chrome Material
mat = bpy.data.materials.new(name="ChromeMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
principled = nodes.get("Principled BSDF")
if principled:
    principled.inputs["Metallic"].default_value = 0.95
    principled.inputs["Roughness"].default_value = 0.15
    if "Base Color" in principled.inputs:
        principled.inputs["Base Color"].default_value = (0.75, 0.85, 1.0, 1.0)
text_obj.data.materials.append(mat)

# Studio Lighting (Three-Point)
# Key Light
key_light = bpy.data.lights.new(name="KeyLight", type='AREA')
key_light.energy = 450
key_obj = bpy.data.objects.new(name="KeyLight", object_data=key_light)
key_obj.location = (4, -4, 4)
bpy.context.collection.objects.link(key_obj)

# Rim Light
rim_light = bpy.data.lights.new(name="RimLight", type='SPOT')
rim_light.energy = 750
rim_obj = bpy.data.objects.new(name="RimLight", object_data=rim_light)
rim_obj.location = (-3, 3, 3)
bpy.context.collection.objects.link(rim_obj)

# Render Output
scene.render.filepath = "/Users/brane/Downloads/aquascape-site/antigravity-video-studio/assets/visuals/scene_blender.png"
bpy.ops.render.render(write_still=True)
print("✅ Blender render complete: /Users/brane/Downloads/aquascape-site/antigravity-video-studio/assets/visuals/scene_blender.png")
