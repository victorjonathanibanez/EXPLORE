'''import os
import glob
import cv2
import numpy as np

class VideoDistributor:
    def __init__(self):
        self.frame_list = []

    def vid_distributor(self, project_path, project_name, background_coords, video_list, time, target_time):
        frames_per_sec = self.get_frames_per_sec(video_list[0])
        start = 15
        time_per_vid = target_time / len(video_list)
        cut_per_min = int((time_per_vid / time) * frames_per_sec * 60)
        frames_per_min = int(1 * frames_per_sec * 60)

        for video in video_list:
            for i in range(1, time + 1):
                end = start + cut_per_min
                frames = self.extract_frames(video, background_coords, start, end)
                self.frame_list.extend(frames)
                start = start + frames_per_min

            start = 15

        self.write_video(project_path, project_name)

    def get_frames_per_sec(self, video_path):
        vidcap = cv2.VideoCapture(video_path)
        frames_per_sec = vidcap.get(cv2.CAP_PROP_FPS)
        vidcap.release()
        return frames_per_sec

    def extract_frames(self, video_path, background_coords, start, end):
        frame_list = []
        vidcap = cv2.VideoCapture(video_path)
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, start)
        success, image = vidcap.read()
        cnt = 1

        while success and cnt <= (end - start):
            cropped_img = image[background_coords[1]:background_coords[3], background_coords[0]:background_coords[2]]
            resized_img = cv2.resize(cropped_img, dsize=(300, 300), interpolation=cv2.INTER_CUBIC)
            frame_list.append(resized_img)
            success, image = vidcap.read()
            cnt += 1

        vidcap.release()
        return frame_list

    def write_video(self, project_path, project_name):
        height, width, depth = self.frame_list[0].shape
        size = (width, height)
        out = cv2.VideoWriter(
            os.path.join(project_path, project_name, project_name) + '.MP4',
            cv2.VideoWriter_fourcc(*'MP4V'),
            15,
            size
        )

        for i in range(len(self.frame_list)):
            out.write(self.frame_list[i])

        out.release()

if __name__ == "__main__":
    # Define parameters
    project_path = "/Users/victor/Desktop/work/"
    project_name = "test_project"
    background_coords = (134, 12, 373, 256) 
    video_list = ['/Volumes/VERBATIM_HD/NOR/same_object_30092020/1-converted.avi','/Volumes/VERBATIM_HD/NOR/same_object_30092020/2-converted.avi']
    time = 4  # Define the time in minutes
    target_time = 2  # Define the target time in minutes

    # Instantiate VideoDistributor class
    distributor = VideoDistributor()

    # Call the vid_distributor method
    distributor.vid_distributor(project_path, project_name, background_coords, video_list, time, target_time)'''

import os
import cv2

class VideoDistributor:
    def __init__(self):
        self.frame_list = []

    def vid_distributor(self, project_path, project_name, background_coords, video_list, time, target_time):
        frames_per_sec = self.get_frames_per_sec(video_list[0])
        frames_per_min = int(frames_per_sec * 60)
        cut_per_min = int((target_time / len(video_list) / time) * frames_per_sec * 60)

        for video in video_list:
            for _ in range(time):
                frames = self.extract_frames(video, background_coords, cut_per_min)
                self.frame_list.extend(frames)

        self.write_video(project_path, project_name)

    def get_frames_per_sec(self, video_path):
        vidcap = cv2.VideoCapture(video_path)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        vidcap.release()  # Release the video capture object
        return fps

    def extract_frames(self, video_path, background_coords, cut_per_min):
        frame_list = []
        vidcap = cv2.VideoCapture(video_path)
        success, image = vidcap.read()
        cnt = 1

        while success and cnt <= cut_per_min:
            cropped_img = image[background_coords[1]:background_coords[3], background_coords[0]:background_coords[2]]
            resized_img = cv2.resize(cropped_img, dsize=(300, 300), interpolation=cv2.INTER_CUBIC)
            frame_list.append(resized_img)
            success, image = vidcap.read()
            cnt += 1

        vidcap.release()  # Release the video capture object
        return frame_list

    def write_video(self, project_path, project_name):
        height, width, _ = self.frame_list[0].shape
        size = (width, height)
        out = cv2.VideoWriter(
            os.path.join(project_path, project_name, project_name) + '_label_video.MP4',
            cv2.VideoWriter_fourcc(*'MP4V'),
            15,
            size
        )

        for frame in self.frame_list:
            out.write(frame)

        out.release()

if __name__ == "__main__":
    # Define parameters
    project_path = "/Users/victor/Desktop/work/"
    project_name = "test_project"
    background_coords = (134, 12, 373, 256) 
    video_list = ['/Volumes/VERBATIM_HD/NOR/same_object_30092020/1-converted.avi',
                  '/Volumes/VERBATIM_HD/NOR/same_object_30092020/2-converted.avi']
    time = 4  # Define the time in minutes
    target_time = 2  # Define the target time in minutes

    # Instantiate VideoDistributor class
    distributor = VideoDistributor()

    # Call the vid_distributor method
    distributor.vid_distributor(project_path, project_name, background_coords, video_list, time, target_time)
