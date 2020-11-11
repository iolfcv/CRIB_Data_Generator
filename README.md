# CRIB Data Generator
<p align="center">
Training Data - Learning Exposure

<img src="https://i.imgur.com/w2DhaHi.gif" width="125" hspace="10"/> <img src="https://i.imgur.com/YUgapi0.gif" width="125" hspace="10"/> <img src="https://i.imgur.com/4LCT3EX.gif" width="125" hspace="10"/> <img src="https://i.imgur.com/ZHO82dX.gif" width="125" hspace="10"/> <img src="https://i.imgur.com/1CSifc0.gif" width="125" hspace="10"/> 
</p>
<p align="center">
Testing Data - Random Views

<img src="https://i.imgur.com/DHwE9Ky.gif" width="125" hspace="10"/> <img src="https://i.imgur.com/kdeZprM.gif" width="125" hspace="10"/> <img src="https://i.imgur.com/xj8qEGi.gif" width="125" hspace="10"/> <img src="https://i.imgur.com/jncaBfj.gif" width="125" hspace="10"/> <img src="https://i.imgur.com/7lmZCeF.gif" width="125" hspace="10"/> 
</p>


This repository contains a set of Python and Blender scripts for data generation in [Incremental Object Learning from Contiguous Views](http://openaccess.thecvf.com/content_CVPR_2019/html/Stojanov_Incremental_Object_Learning_From_Contiguous_Views_CVPR_2019_paper.html)

## Initial Setup
Follow [setup instructions](https://github.com/iolfcv/CRIB_Data_Generator/blob/master/SETUP.md) readme.

## Quick Demo Commands
``` 
python generate_data.py -start=0 -end=1 
```
Generates one small learning exposure in `train_data` and testing samples in `test_data` of one object on a blank background.
``` 
python generate_data_pose_list.py -start=0 -end=1 
```
Make sure to execute these commands in the main repository directory, not `./CRIB`.
Generates 10 frames of one object rotating in the tilt direction (euler coordinates), specified in `pose_list.json`.
## Generating Data as in the Paper
1. In `data_generation_parameters.json` specify `"total_frames":100` and `"background":"blank"` or `"background":"clutter"` depending on background preference.
2. ```python generate_data.py ```

## Generating Data From Specified Pose
1. Use `create_pose_json.py` to generate a `pose_list.json` file which will contain the `[azimuth, elevation, tilt, scale]` per frame of the data you would like to render.
2. Example command to render 10 objects according to pose specified in `pose_list.json` 
```python generate_data_pose_list.py -start=0 -end=10```

## Additional Notes
1. If using GPUs to render, specify bigger a render tile size in `data_generation_parameters.json` to speed up rendering, and similarly a smaller one if using CPU.

## Citation
If you use this code, please cite our work :
```
@InProceedings{Stojanov_2019_CVPR,
author = {Stojanov, Stefan and Mishra, Samarth and Anh Thai, Ngoc and Dhanda, Nikhil and Humayun, Ahmad and Yu, Chen and Smith, Linda B. and Rehg, James M.},
title = {Incremental Object Learning From Contiguous Views},
booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
month = {June},
year = {2019}
} 
```
