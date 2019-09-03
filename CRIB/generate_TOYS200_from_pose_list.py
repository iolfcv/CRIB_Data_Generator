import bpy
import numpy as np
import sys
import os
import pdb
import json

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
    
    model_name   = sys.argv[mn_fr_idx]

    ''' =========================== '''
    
    ''' load some render config things '''

    with open('data_generation_parameters.json') as load_file:
        data_gen_params = json.load(load_file)        
    
    render_parameters = data_gen_params['render_parameters']
    light_parameters = data_gen_params['light_parameters']
    learning_exp_properties = data_gen_params['learning_exp_properties']

    ''' ============================== '''

    ''' load pose list '''
    
    with open('pose_list.json') as load_file:
        pose_list = json.load(load_file)['pose_list']
    
    ''' ============== '''
     
    total_frames = learning_exp_properties['total_frames']
    total_points = learning_exp_properties['total_points']

    # Get context elements: scene and object
    scn = bpy.context.scene
    toy_obj = bpy.data.objects[model_name]
    cam = bpy.data.objects['Camera']

    #making sure correct object is visible
    toy_obj.hide = True
    toy_obj.hide_render = False
    
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
    output_path = os.path.abspath('./pose_list_data/{}/'.format(toy_obj.name))
    
    image_output.base_path = os.path.join(output_path)

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
   
    for frame_idx, (azim, elev, tilt, scale) in enumerate(pose_list):            

            scn.frame_set(frame_idx)

            toy_obj.rotation_euler[0] = elev
            toy_obj.rotation_euler[1] = azim
            toy_obj.rotation_euler[2] = tilt

            #scl = np.random.uniform(0.3,1.1)
            
            toy_obj.scale = (scale, scale, scale)

            bpy.context.scene.update()

            bpy.ops.render.render()

if __name__ == "__main__":
    generate()
    print("BLENDER MAIN DONE")
