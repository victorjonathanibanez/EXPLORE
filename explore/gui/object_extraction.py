import cv2
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

class ObjectExtractor:
    def __init__(self):
        self.image = None
        self.ref_point = []
        self.crop = False
        self.root = None

    def grep_frame(self, video, ref):
        vidcap = cv2.VideoCapture(video)
        success, image = vidcap.read()
        count = 1

        while success:
            if count == 50:
                res1 = image[ref[0][1]:ref[1][1], ref[0][0]:ref[1][0]]
                return res1
                break

            success, image = vidcap.read()
            count += 1

    def shape_selection(self, event, x, y, flags, param):
        global ref_point
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ref_point = [(x, y)]
        elif event == cv2.EVENT_LBUTTONUP:
            self.ref_point.append((x, y))
            cv2.rectangle(self.image, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
            cv2.imshow("draw rectangle around current object / 'r' for again / 'c' for crop", self.image)
            cv2.putText(self.image, o, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3, cv2.LINE_AA, False)

    def main(self, video, ref, o):
        self.image = self.grep_frame(video, ref)
        self.ref_point = []
        self.crop = False
        clone = self.image.copy()
        cv2.namedWindow("draw rectangle around current object / 'r' for again / 'c' for crop", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("draw rectangle around current object / 'r' for again / 'c' for crop", self.shape_selection)
        cv2.startWindowThread()

        while True:
            cv2.imshow("draw rectangle around current object / 'r' for again / 'c' for crop", self.image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):
                self.image = clone.copy()
            elif key == ord("c"):
                break

        if len(self.ref_point) == 2:
            crop_img = clone[self.ref_point[0][1]:self.ref_point[1][1], self.ref_point[0][0]:self.ref_point[1][0]]

        cv2.destroyAllWindows()

        return self.ref_point
