import bpy

# --- Step 1: Create Armature and Bones ---
armature = bpy.data.armatures.new("CharacterArmature")
armature_obj = bpy.data.objects.new("Character", armature)
bpy.context.collection.objects.link(armature_obj)
bpy.context.view_layer.objects.active = armature_obj
bpy.ops.object.mode_set(mode='EDIT')

edit_bones = armature.edit_bones
spine = edit_bones.new("Spine")
spine.head = (0, 0, 0)
spine.tail = (0, 0, 1)

head = edit_bones.new("Head")
head.head = spine.tail
head.tail = (0, 0, 1.5)
head.parent = spine

bpy.ops.object.mode_set(mode='OBJECT')

# --- Step 2: Add Mesh and Parent to Armature ---
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
mesh_obj = bpy.context.active_object

mesh_obj.select_set(True)
armature_obj.select_set(True)
bpy.context.view_layer.objects.active = armature_obj
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# --- Step 3: Animate Head Bone ---
bpy.context.view_layer.objects.active = armature_obj
bpy.ops.object.mode_set(mode='POSE')

pose_head = armature_obj.pose.bones["Head"]
pose_head.rotation_mode = 'XYZ'

# Frame 1: Tilt up
pose_head.rotation_euler = (0.2, 0, 0)
pose_head.keyframe_insert(data_path="rotation_euler", frame=1)

# Frame 20: Tilt down
pose_head.rotation_euler = (-0.2, 0, 0)
pose_head.keyframe_insert(data_path="rotation_euler", frame=20)

bpy.ops.object.mode_set(mode='OBJECT')
