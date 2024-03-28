# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------
# ORT analysis - main script training - developed by Victor Ibañez
# 03.04.2021
# -------------------------------------------------------------------------------------

import os
from tkinter import *
from tkinter import filedialog

#import tkinter as Tk
#from tkinter import simpledialog, filedialog
from gui.training import TrainingGUI
#from utils.random_distribution import RandomDistributor
from gui.bounding_box import BoundingBoxGUI
from gui.object_extraction import ObjectExtractor
from video_distribution import VideoDistributor
from video_scroll import VideoScroll
from utils.raw_data_creation import RawDataCreator
from utils.training_data_creation import TrainingDataCreator
from models.multi_class_network import MultiClassNetworkTrainer
import shutil

def main():
    # Get project settings from GUI_training class
    root = Tk()
    training_gui = TrainingGUI(root)
    root.mainloop()
    data_from_gui = training_gui.submitted_data
    print(data_from_gui)
    project_name = data_from_gui['Project Name']
    project_path = data_from_gui['Project Path']
    videos_path = data_from_gui['Videos Path'].split('\n')
    videos_length = data_from_gui['Video Length']
    manual_scoring_video_length = data_from_gui['Manual Scoring Video Length']
    objects_dict = dict(data_from_gui['Objects'])

    #time = int(time)
    #ttime = int(ttime)

    project_folder = os.path.join(project_path, project_name)
    
    # Create project folder if it doesn't exist
    #if not os.path.isdir(project_folder):
        #os.makedirs(project_folder)


    # Extract training frames
    #ref_point = ObjectSelector().main(videos_path[0])
    gui = BoundingBoxGUI(videos_path[0], objects_dict)
    bounding_boxes = gui.get_bounding_boxes()
    print(bounding_boxes)

    # Create sampled video
    print('creating video for labeling...')
    VideoDistributor.vid_distributor(project_path, project_name, ref_point, videos, time, ttime)

    # Define label paths
    label_path = os.path.join(project_folder, 'labeled')

    if not os.path.isdir(label_path):
        os.makedirs(label_path)

    names = objects
    keys = o_keys

    obj_key = {names[i]: keys[i] for i in range(len(names))}

    for i in names:
        path = os.path.join(label_path, i)
        if not os.path.isdir(path):
            os.makedirs(path)

    no_path = os.path.join(label_path, 'no')

    if not os.path.isdir(no_path):
        os.makedirs(no_path)

    vid = os.path.join(project_path, project_name, project_name) + '.MP4'

    # Hand label video
    video_scroll_obj = VideoScroll()
    dic = video_scroll_obj.initialize_video_scroll(vid, names, keys)

    # Write logfile
    L = ['project: \n', project_name, '\n', '\n',
         'sampled videos: \n', str(videos), '\n', '\n',
         'video duration: \n', str(time), '\n', '\n',
         'cropping coordinates: \n', str(ref_point), '\n', '\n',
         'objects: \n', str(obj_key), '\n', '\n',
         'iteration: \n', str(1), '\n', '\n',
         'trained frames: \n', str(dic)]

    with open(os.path.join(project_folder, 'logfile'), "w+") as f:
        f.writelines(L)

    # Create raw data
    print('create raw data...')
    raw_data_creator = RawDataCreator()
    raw_data_creator.create_raw_data(vid, label_path, dic)

    # Define training and plot paths
    training_path = os.path.join(project_folder, 'training')
    plot_path = os.path.join(project_folder, 'plots')

    if not os.path.isdir(training_path):
        os.makedirs(training_path)

    if not os.path.isdir(plot_path):
        os.makedirs(plot_path)

    # Create training data
    print('create training data...')
    training_data_creator = TrainingDataCreator()
    training_data_creator.create_training_data(label_path, training_path, names)

    # Train the network
    print('train the network...')
    multi_class_trainer = MultiClassNetworkTrainer()
    multi_class_trainer.train_multi_class_network(label_path, training_path, project_path, project_name, plot_path)

    # Delete training data
    try:
        shutil.rmtree(training_path)
    except OSError as e:
        print("Error: %s : %s" % (training_path, e.strerror))

if __name__ == "__main__":
    main()
