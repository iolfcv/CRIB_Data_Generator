import bpy
import numpy as np
import sys
import os
import pdb
import argparse
import copy
import json

from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

# ENABLE GPU'S FROM BLENDER PREFERENCES
bpy.context.user_preferences.addons['cycles'].preferences['compute_device_type'] = 1

# blender doesn't see local paths, so we need to add the directory where the lamps module is 
sys.path.append('CRIB')
import lamps

def plus_minus(val, percent = 100):
    '''
        randomly scale a vlalue up or down by <percent>
    '''
    percent = percent / 100.0
    coin = np.random.choice([True, False])
    
    if coin:
        val = val + val*percent
    else:
        val = val - val*percent
    
    return val

def generate():
    ''' ========= argparse ========''' 
    try:
        mn_fr_idx = sys.argv.index("model_name") + 1
    except ValueError:
        print("No argument passed for model name)")
        exit()
    
    try: ncls_idx = sys.argv.index("n_exposures") + 1
    except ValueError:
            print("No argument passed for n_exposures")

    model_name   = sys.argv[mn_fr_idx]
    n_exposures  = int(sys.argv[ncls_idx])

    ''' =========================== '''
    
    ''' load some render config things '''

    with open('data_generation_parameters.json') as load_file:
        data_gen_params = json.load(load_file)        
    
    render_parameters = data_gen_params['render_parameters']
    light_parameters = data_gen_params['light_parameters']
    learning_exp_properties = data_gen_params['learning_exp_properties']

    ''' ============================== '''
    
    total_frames = learning_exp_properties['total_frames']
    total_points = learning_exp_properties['total_points']

    # Get context elements: scene and object
    scn = bpy.context.scene
    obj = bpy.data.objects[model_name]
    cam = bpy.data.objects['Camera']

    #making sure correct object is visible
    obj.hide = True
    obj.hide_render = False
    
    #random frames to place random pose and then interpolate
    frame_idx = np.random.randint(1,total_frames,total_points)

    # make sure first frame's first and last frame's last
    frame_idx[0] = 0
    frame_idx[-1] = total_frames-1
    frame_idx.sort()

    # HARDCODED : threshold for below which frames aren't directly interpolated to
    frame_threshold = 40
    
    scn.frame_end = total_frames-1

    ''' ========= misc settings ======== '''
    
    bpy.context.scene.render.resolution_x = render_parameters['resolution']
    bpy.context.scene.render.resolution_y = render_parameters['resolution']
    scn.render.resolution_percentage = render_parameters['resolution_percentage']
    scn.render.layers['RenderLayer'].samples = render_parameters['render_samples']
    scn.cycles.debug_use_spatial_splits = render_parameters['use_spatial_splits']
    scn.cycles.max_bounces = render_parameters['max_bounces']
    scn.cycles.min_bounces = render_parameters['min_bounces']
    scn.cycles.transparent_max_bounces = render_parameters['transparent_max_bounces']
    scn.cycles.transparent_min_bounces = render_parameters['transparent_min_bounces']
    scn.cycles.glossy_bounces = render_parameters['glossy_bounces']
    scn.cycles.transmission_bounces = render_parameters['transmission_bounces']
    scn.render.use_persistent_data = render_parameters['use_persistent_data']
    scn.render.tile_x = render_parameters['render_tile_x']
    scn.render.tile_y = render_parameters['render_tile_y']
    scn.cycles.caustics_refractive = render_parameters['use_caustics_refractive']
    scn.cycles.caustics_reflective = render_parameters['use_caustics_reflective']
    scn.cycles.device = render_parameters['rendering_device']
    scn.render.image_settings.color_mode = render_parameters['color_mode']
    scn.render.layers['RenderLayer'].cycles.use_denoising = render_parameters['use_denoising']
    scn.render.layers['RenderLayer'].cycles.denoising_radius = render_parameters['denoising_radius']
    scn.cycles.film_transparent = render_parameters['use_film_transparent']
    
    ''' ================================ '''


    '''paths''' 
    tree = bpy.context.scene.node_tree
    image_output = tree.nodes['Image_Output']
    output_path = os.path.abspath('./train_data/{}/{}'.format(obj.name, str(n_exposures)))
    
    image_output.base_path = output_path

    ''' ======== adding lamps and jittering them ======== '''
    
    #hard coded location
    area_locations = light_parameters['area_light_locations']
    point_locations = light_parameters['point_light_locations']

    #choice between rod lamps or points
    point_or_area = np.random.choice([True, False])

    if point_or_area == True:
            temp = np.random.randint(light_parameters['light_temperature_range'][0],
                                     light_parameters['light_temperature_range'][1])

            strength = np.random.randint(light_parameters['point_strength_range'][0],
                                         light_parameters['point_strength_range'][1])

            for location in point_locations:
                    lamps.make_point_lamp(location,
                                          strength = plus_minus(strength,percent=50), 
                                          temp = temp, 
                                          jitter_location = True)

    if point_or_area == False:
            temp = np.random.randint(light_parameters['light_temperature_range'][0],
                                     light_parameters['light_temperature_range'][1])

            strength = np.random.randint(light_parameters['area_strength_range'][0],
                                         light_parameters['area_strength_range'][1])

            for location in area_locations:
                    location = (plus_minus(location[0],80),
                                plus_minus(location[1],80),
                                location[2])
                    lamps.make_area_lamp(location, 
                                         size_x = 3, 
                                         size_y = 0.1, 
                                         strength = plus_minus(strength,percent=50), 
                                         temp = temp, 
                                         jitter_rotation = True)
    
    ''' ================================================= '''
    
    ''' ======== jittering scale ======== '''
    scl = np.random.uniform(0.6,0.7333)

    scl = [plus_minus(scl, np.random.randint(0,50)) for _ in np.arange(total_points)]
    
    ''' ================================= '''
    
    ''' ========= procedurally animate the motion ======== '''
    for i, frame in enumerate(frame_idx):
            if i>0 and frame - frame_idx[i-1] < frame_threshold:
                    # take frame_threshold frames and interpolate and cut at the required number of frames
                    frame_repl = frame_threshold + frame_idx[i-1]
            else:
                    frame_repl = frame

            scn.frame_set(frame_repl)
            print(frame)
            x = np.random.uniform(-3.14,3.14,1)[0]
            y = np.random.uniform(-3.14,3.14,1)[0]
            z = np.random.uniform(0,6.28,1)[0]

            obj.rotation_euler[0] = x
            obj.rotation_euler[1] = y
            obj.rotation_euler[2] = z

            #scaling
            obj.scale = (scl[i],scl[i],scl[i])

            obj.keyframe_insert(data_path='rotation_euler',frame = frame_repl)
            obj.keyframe_insert(data_path='scale',frame = frame_repl)

            for fcurve in obj.animation_data.action.fcurves:
                    kf = fcurve.keyframe_points[-1]
                    kf.interpolation = 'LINEAR'

            if i>0 and frame - frame_idx[i-1] < frame_threshold:
                    scn.frame_set(frame)
                    obj.keyframe_insert(data_path='rotation_euler',frame = frame)
                    obj.keyframe_insert(data_path='scale',frame = frame)

                    obj.keyframe_delete(data_path='rotation_euler', frame = frame_repl)
                    obj.keyframe_delete(data_path='scale', frame = frame_repl)

            for fcurve in obj.animation_data.action.fcurves:
                    kf = fcurve.keyframe_points[-1]
                    kf.interpolation = 'LINEAR'

    ''' ================================================== '''
    
    ''' reset sequence start and end then render '''
 
    scn.frame_start = 0
    scn.frame_end = total_frames-1
    
    bpy.ops.render.render(animation=True)
    
    ###  ========= gather scene metadata ======== ###
    pose_ls = []
    scale_ls = []
    for fr_idx in np.arange(total_frames):
        scn.frame_set(fr_idx)
        pose_ls.append(copy.deepcopy(obj.rotation_euler))
        scale_ls.append(copy.deepcopy(obj.scale))

    scn_lamps = [obj for obj in bpy.data.objects if obj.type == 'LAMP'] 
    
    lamp_names = [obj.name \
                  for obj in scn_lamps]
    
    lamp_strengths = [obj.data.node_tree.nodes[1].inputs[1].default_value \
                      for obj in scn_lamps]
    
    lamp_temps = [obj.data.node_tree.nodes[0].inputs[0].default_value \
                  for obj in scn_lamps]
    
    lamp_locations = [obj.location \
                     for obj in scn_lamps]
    lamp_rotations = [obj.rotation_euler \
                     for obj in scn_lamps]
    
    metadata_to_save = {
        'obj_pose' : [list(x) for x in pose_ls],
        'obj_scale' : [list(x) for x in scale_ls],
        'lamp_names' : lamp_names,
        'lamp_strengths' : lamp_strengths,
        'lamp_temps' : lamp_temps,
        'lamp_locations' : [list(x) for x in lamp_locations],
        'lamp_rotations' : [list(x) for x in lamp_rotations]
        }

    out_path = os.path.abspath('./render_data/{}/{}/metadata.json'.format(obj.name, str(n_exposures)))
    out_str = json.dumps(metadata_to_save)

    with open(out_path, 'w') as out_file:
        out_file.write(out_str)

    ### ======================================== ###
    
if __name__ == "__main__":
    generate()
    print("BLENDER MAIN DONE")
    

