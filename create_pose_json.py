import json
import numpy as np

scale = 1

obj_pose_dict = {}

pose_list_azim = [[azimuth, 0,         0   , scale] for azimuth in np.linspace(0, 6.28, 10)]
pose_list_elev = [[0,       elevation, 0   , scale] for elevation in np.linspace(0, 6.28, 10)]
pose_list_tilt = [[0,       0,         tilt, scale] for tilt in np.linspace(0, 6.28, 10)]

obj_pose_dict['pose_list'] = pose_list_tilt

out_string = json.dumps(obj_pose_dict, indent=4)

with open('pose_list.json', 'w') as output_file:
    output_file.write(out_string)

