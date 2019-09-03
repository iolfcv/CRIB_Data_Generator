import os, time, pickle
import numpy as np
import pdb
import json

def wrapper_train_data(model_name, n_exposures):
        # getting blender path from .json
        with open('data_generation_parameters.json') as load_file:
            data_gen_params = json.load(load_file)        
        blender = data_gen_params['blender_path']

        start_time = time.time()
        # relative path
        blender_script_path = 'CRIB/generate_TOYS200_train.py'
        blendfile_path = os.path.join(os.getcwd(), 'generate_scene_CRIB.blend')
        
        cmd =  '{} -noaudio --background {} ' \
               '--python {} ' \
               'model_name {} ' \
               'n_exposures {} ' \
               '1>/dev/null'.format(
                blender, 
                blendfile_path, 
                blender_script_path, 
                model_name, 
                n_exposures)

        os.system(cmd)
        
        resolution = data_gen_params['render_parameters']['resolution']
        total_frames = data_gen_params['learning_exp_properties']['total_frames']

        print('--- rendered {} {}x{} frames of model {} in {:.2f} seconds ---'.format(
            total_frames, 
            resolution, 
            resolution,
            model_name, 
            time.time() - start_time))

def wrapper_test_data(model_name):
        # getting blender path from .json
        with open('data_generation_parameters.json') as load_file:
            data_gen_params = json.load(load_file)        
        
        blender = data_gen_params['blender_path']

        # to measure total time
        start_time = time.time()
        # relative path
        blender_script_path = 'CRIB/generate_TOYS200_test.py'
        blendfile_path = os.path.join(os.getcwd(), 'generate_scene_CRIB.blend')
        
        cmd =  '{} -noaudio --background {} ' \
               '--python {} ' \
               'model_name {} ' \
               '1>/dev/null'.format(
                blender, 
                blendfile_path, 
                blender_script_path, 
                model_name)

        os.system(cmd)
        
        resolution = data_gen_params['render_parameters']['resolution']
        total_frames = data_gen_params['learning_exp_properties']['total_frames']

        print('--- rendered {} {}x{} frames of model {} in {:.2f} seconds ---'.format(
            total_frames, 
            resolution, 
            resolution,
            model_name, 
            time.time() - start_time))

def wrapper_pose_list_data(model_name):
        # getting blender path from .json
        with open('data_generation_parameters.json') as load_file:
            data_gen_params = json.load(load_file)        
        
        blender = data_gen_params['blender_path']
        
        with open('pose_list.json') as load_file:
            pose_list = json.load(load_file)['pose_list']
        
        total_frames = len(pose_list)

        # to measure total time
        start_time = time.time()
        # relative path
        blender_script_path = 'CRIB/generate_TOYS200_from_pose_list.py'
        blendfile_path = os.path.join(os.getcwd(), 'generate_scene_CRIB.blend')
        
        cmd =  '{} -noaudio --background {} ' \
               '--python {} ' \
               'model_name {} ' \
               '1>/dev/null'.format(
                blender, 
                blendfile_path, 
                blender_script_path, 
                model_name)

        os.system(cmd)
        
        resolution = data_gen_params['render_parameters']['resolution']

        print('--- rendered {} {}x{} frames of model {} in {:.2f} seconds ---'.format(
            total_frames, 
            resolution, 
            resolution,
            model_name, 
            time.time() - start_time))

def get_bbox(img):

    img = np.asarray(img)

    horz = np.sum(img, axis = 0)
    vert = np.sum(img, axis = 1)

    horz = np.where(horz[:,3] >= 5)
    vert = np.where(vert[:,3] >=5)

    x_min = horz[0][0]
    x_max = horz[0][-1]
    y_min = vert[0][0]
    y_max = vert[0][-1]
    
    return [x_min, x_max, y_min, y_max]

def transparent_overlay(overlay,src):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    """
    h,w,_ = overlay.shape  # Size of foreground
    rows,cols,_ = src.shape  # Size of background Image
    
    alpha = overlay[:,:,3]/255.0
    src[:,:,0] = np.multiply(alpha,overlay[:,:,0]) + np.multiply((1-alpha),src[:,:,0])
    src[:,:,1] = np.multiply(alpha,overlay[:,:,1]) + np.multiply((1-alpha),src[:,:,1])
    src[:,:,2] = np.multiply(alpha,overlay[:,:,2]) + np.multiply((1-alpha),src[:,:,2])

    return src
