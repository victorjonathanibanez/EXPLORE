#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------
# ORT analysis - script random distributor - developed by Victor Ibañez
# 03.04.2021
# -------------------------------------------------------------------------------------

# -----------------------------------------------------
# import libraries
# -----------------------------------------------------
import os
import cv2
import numpy as np
import random
from sklearn.cluster import KMeans

class RandomDistributor:
    def __init__(self):
        self.image_array = []

    def read_video_frames(self, video_path):
        vidcap = cv2.VideoCapture(video_path)
        success, image = vidcap.read()
        cnt = 1

        while success:
            if cnt == 50:
                img = image[:, :, 0]
                img = np.concatenate(img)
                self.image_array.append(img)
            elif cnt > 50:
                break

            success, image = vidcap.read()
            cnt += 1

    def apply_kmeans(self, vids, nk):
        for video in vids:
            self.read_video_frames(video)

        kmeans = KMeans(n_clusters=nk, random_state=0).fit(self.image_array)

        clusters = set(kmeans.labels_)
        cluster_dict = {}

        for video, label in zip(vids, kmeans.labels_):
            for cluster in clusters:
                if cluster == label:
                    if cluster in cluster_dict:
                        cluster_dict[cluster].append(video)
                    else:
                        cluster_dict[cluster] = [video]

        selected_videos = [random.choice(cluster_dict[cluster]) for cluster in cluster_dict]

        return selected_videos

if __name__ == "__main__":
    def main():
        # Example usage
        videos = ["video1.mp4", "video2.mp4", "video3.mp4"]  # Replace with your actual video paths
        num_clusters = 3  # Replace with the desired number of clusters

        distributor = RandomDistributor()
        selected_videos = distributor.apply_kmeans(videos, num_clusters)

        print("Selected Videos:")
        for video in selected_videos:
            print(video)

    main()
