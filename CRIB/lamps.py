'''
fname = '/home/sstojanov3/Desktop/lighting_schemes/lamps.py'
exec(compile(open(fname).read(), fname, 'exec'))
'''
import bpy
import numpy as np

def delete_lamps():
	import bpy
	# deselect all
	bpy.ops.object.select_all(action='DESELECT')

	# selection and deletion
	for obj in bpy.data.objects:

		if obj.type == 'LAMP':
			obj.select = True
			bpy.ops.object.delete()

def make_point_lamp(location, strength = 100, temp = 5000, jitter_location = False):

	if jitter_location == True:
		location = location + np.random.uniform(-1,1,3)

	bpy.ops.object.lamp_add(type='POINT', view_align=False, location=location, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))


	lamp = bpy.data.lamps[bpy.context.active_object.name]
	nodes = lamp.node_tree.nodes

	for node in nodes:
		nodes.remove(node)

	node_blackbody = nodes.new(type= 'ShaderNodeBlackbody')
	node_emission  = nodes.new(type = 'ShaderNodeEmission')
	node_output    = nodes.new(type = 'ShaderNodeOutputLamp')

	node_output.location[1] = 400
	node_emission.location[1] = 200

	lamp.node_tree.links.new(node_blackbody.outputs[0],node_emission.inputs[0])
	lamp.node_tree.links.new(node_emission.outputs[0], node_output.inputs[0])

	node_emission.inputs[1].default_value = strength
	node_blackbody.inputs[0].default_value = temp

def make_area_lamp(location, size_x = 0, size_y = 0, strength = 10, temp = 5000, jitter_rotation = False):

	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=location, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

	lamp = bpy.data.lamps[bpy.context.active_object.name]
	lamp.shape  = 'RECTANGLE'
	lamp.size   = size_x 
	lamp.size_y = size_y

	nodes = lamp.node_tree.nodes

	for node in nodes:
		nodes.remove(node)

	node_blackbody = nodes.new(type= 'ShaderNodeBlackbody')
	node_emission  = nodes.new(type = 'ShaderNodeEmission')
	node_output    = nodes.new(type = 'ShaderNodeOutputLamp')

	node_output.location[1] = 400
	node_emission.location[1] = 200

	lamp.node_tree.links.new(node_blackbody.outputs[0],node_emission.inputs[0])
	lamp.node_tree.links.new(node_emission.outputs[0], node_output.inputs[0])

	node_emission.inputs[1].default_value = strength
	node_blackbody.inputs[0].default_value = temp

	if jitter_rotation == True:
		ang = np.random.uniform(-np.radians(60),np.radians(60))
		bpy.context.active_object.rotation_euler[2] = ang

# area_locations = [[0,-2.5,3],[0,0,3],[0,2.5,3]]
# point_locations = [[2.5,2.5,3],[-2.5,2.5,3],[2.5,-2.5,3],[-2.5,-2.5,3]]

# for location in point_locations:
# 	make_point_lamp(location,strength = 300, temp = 5000, jitter_location = False)

# # for location in area_locations:
# # 	make_area_lamp(location, size_x = 3, size_y = 0.1, strength =  100, temp = 5000, jitter_rotation = False)


