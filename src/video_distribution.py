import os
import glob
import cv2
import numpy as np

class VideoDistributor:
    def __init__(self):
        self.frame_list = []

    def vid_distributor(self, project_path, project_name, ref_point, vid_list, time, ttime):
        fps = self.get_fps(vid_list[0])
        target_time = ttime
        start = 15
        t_per_vid = target_time / len(vid_list)
        cut_per_min = int((t_per_vid / time) * fps * 60)
        f_per_min = int(1 * fps * 60)

        for vid in vid_list:
            for i in range(1, time + 1):
                end = start + cut_per_min
                frames = self.extract_frames(vid, ref_point, start, end)
                self.frame_list.extend(frames)
                start = start + f_per_min

            start = 15

        self.write_video(project_path, project_name)

    def get_fps(self, video_path):
        vidcap = cv2.VideoCapture(video_path)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        vidcap.release()
        return fps

    def extract_frames(self, video_path, ref_point, start, end):
        frame_list = []
        vidcap = cv2.VideoCapture(video_path)
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, start)
        success, image = vidcap.read()
        cnt = 1

        while success and cnt <= (end - start):
            res1 = image[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
            res = cv2.resize(res1, dsize=(300, 300), interpolation=cv2.INTER_CUBIC)
            frame_list.append(res)
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
