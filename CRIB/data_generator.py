import sys
import os
import math
import numpy as np
import random
import cv2
import time
import pdb
import json

from CRIB.render_utils import wrapper_train_data
from CRIB.render_utils import wrapper_test_data
from CRIB.render_utils import wrapper_pose_list_data
from CRIB.render_utils import get_bbox, transparent_overlay

class data_generator(object):

    def __init__(self, model_name):
            # setting some variables 
            with open('object_groups.json') as json_file:
                self.models_list = json.load(json_file)['object_groups']

            with open('data_generation_parameters.json') as load_file:
                self.data_gen_params = json.load(load_file)        
                       
            self.model_name = model_name
            self.n_exposures = 0
            
    def get_training_data(self):
            """
            Generates a learning exposure of length <total_frames> in the .json file
            of RGB images, and their respective bounding boxes in "training_data" directory
             """

            wrapper_train_data(self.model_name, self.n_exposures)

            self.bbox_and_overlay("training_data")
            
            self.n_exposures += 1

    def get_testing_data(self):
            """
            Generates a testing data of length <total_frames> in the .json file
            of RGB images, and their respective bounding boxes in "testing_data" directory
            """
           
            wrapper_test_data(self.model_name)

            self.bbox_and_overlay("testing_data")
    
    def get_pose_list_data(self):
            """
            Generates a a sequence of data of length <pose_list> specified in the in the 
            "pose_list.json" file of RGB images. The object is rendered in the poses
            specified in "pose_list.json" on a blank background.
            """
           
            wrapper_pose_list_data(self.model_name)

            self.bbox_and_overlay("pose_list_data")
    
    def bbox_and_overlay(self, data_subset):
        """
        param: string data_subset can be "training data" or "testing data"

        this function obtains bounding boxes and overlays the data either on a cluttered
        or blank background. The clutter vs. blank background can be specified in 
        "data_generation_parameters.json"
        """
        
        if data_subset == "pose_list_data":
            with open('pose_list.json') as load_file:
                pose_list = json.load(load_file)['pose_list']
            
            total_frames = len(pose_list)

        else:
            total_frames = self.data_gen_params['learning_exp_properties']['total_frames']

        resolution = self.data_gen_params['render_parameters']['resolution']
        background = self.data_gen_params['background']

        bboxes = np.zeros((total_frames, 4))
        bck_idx = self.choose_background()

        for frame in range(total_frames):

            # reading rendedered image and finding bbox
            img, im_filepath = self.read_img(frame, data_subset)
            bbox = get_bbox(img)

            if data_subset == "testing_data":
                random_idx = np.random.randint(0,200)
                bck_filepath = os.path.join('backgrounds', 
                                            'background{}'.format(bck_idx), 
                                            '{:04d}.png'.format(random_idx))
            
            elif data_subset == "training_data":
                bck_filepath = os.path.join('backgrounds',
                                                'background{}'.format(bck_idx), 
                                                '{:04d}.png'.format(frame))
            elif data_subset == "pose_list_data":
                bck_filepath = None

            else:
                raise Exception("data_subset can be either " + \
                                "\"training_data\" or \"testing data\"")

            # overlaying background            
            if background == 'blank':
                bck = np.ones((resolution, resolution, 3))*200
            elif background == 'clutter':
                bck = cv2.imread(bck_filepath)
                bck = cv2.resize(bck, (resolution, resolution))
            else:
                raise NameError("background in data_generation_parameters.json " +\
                                "can be \"blank\" or \"clutter\"")

            #bck = np.ones((resolution, resolution, 3))*255

            img = transparent_overlay(img,bck)

            #adding a bit of noise
            noise_image = np.zeros((resolution, resolution,4), np.uint8)
            noise_image[:,:,0:3] = np.random.randint(0,255, (resolution, resolution,3))
            noise_image[:,:,3] = np.ones((resolution, resolution))*10

            #ovelaying noise
            img = transparent_overlay(noise_image, img)
            cv2.imwrite(im_filepath, img)
        
        if data_subset == "training_data": 
            np.save(os.path.join('train_data', 
                                 str(self.model_name), 
                                 str(self.n_exposures), 
                                 'bboxes.npy'), np.asarray(bboxes))

        elif data_subset == "testing_data":
            np.save(os.path.join("test_data" , 
                                 str(self.model_name), 
                                 "bboxes.npy"), np.asarray(bboxes))
        
        elif data_subset == "pose_list_data":
            np.save(os.path.join("pose_list_data" , 
                                 str(self.model_name), 
                                 "bboxes.npy"), np.asarray(bboxes))

    def read_img(self, frame, data_subset):
    
        if data_subset == "testing_data":
            im_filepath = os.path.join('test_data', 
                                           self.model_name, 
                                           '{:04d}.png'.format(frame))
        if data_subset == "pose_list_data":
            im_filepath = os.path.join('pose_list_data', 
                                           self.model_name, 
                                           '{:04d}.png'.format(frame))
       
        elif data_subset == "training_data":
             im_filepath = os.path.join('train_data', 
                                           self.model_name, 
                                           str(self.n_exposures), 
                                           '{:04d}.png'.format(frame))
        try:
             img = cv2.imread(im_filepath, cv2.IMREAD_UNCHANGED)
        except Exception as _err:
            sys.stderr.write("Something went wrong reading file: ".format(im_filepath))
            raise Exception(_err)

        if not isinstance(img, np.ndarray):
            print("Something wrong with file \'{}\'".format(im_filepath))
            raise Exception("File Corrupted")

        return img, im_filepath

    def choose_background(self):
        '''
            this function chooses a background index that does not
            contain the foreground object
        '''
        name = self.model_name
        bools = []
        for ls in self.models_list:
            bools.append(name in ls)
        bck = [i for i, x in enumerate(bools) if x][0] + 1

        r = np.concatenate((np.arange(1,bck), np.arange(bck+1, 9)), axis=0)

        return np.random.choice(r)



