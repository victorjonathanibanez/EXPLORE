import glob
import os
import cv2

class RawDataCreator:
    def __init__(self):
        pass

    def create_raw_data(self, video, path, dic):
        vidcap = cv2.VideoCapture(video)
        success, image = vidcap.read()
        count = 0
        frames_list = []

        while success:
            resized_frame = cv2.resize(image, dsize=(150, 150), interpolation=cv2.INTER_CUBIC)
            frames_list.append(resized_frame)
            success, image = vidcap.read()
            count += 1

        excluded_frames = []

        object_list = list(dic.values())

        for i in range(len(object_list)):
            target_name = list(dic.keys())[i]
            target_path = os.path.join(path, target_name)

            for j in range(0, len(object_list[i]), 2):
                for frame, count in zip((frames_list[object_list[i][j]:object_list[i][j + 1] + 1]),
                                        range(object_list[i][j], object_list[i][j + 1] + 1)):
                    cv2.imwrite(os.path.join(target_path, f"{target_name}_{count}.jpg"), frame)
                    excluded_frames.append(count)

        for i in range(len(frames_list)):
            if i not in excluded_frames:
                cv2.imwrite(os.path.join(path, 'no', 'no') + f"_{i}.jpg", frames_list[i])


# Example Usage:
# raw_data_creator = RawDataCreator()
# raw_data_creator.create_raw_data('your_video.mp4', 'output_path', {'Object1': [start1, end1, start2, end2, ...], 'Object2': [...], ...})
