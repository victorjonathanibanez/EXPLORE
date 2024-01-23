import cv2
import numpy as np
import os

class VideoScroll:
    def __init__(self):
        self.dic = {}
        self.n_dic = {}
        self.top_label = ""
        self.cnt = 0
        self.reset = 0
        self.show = 0
        self.compare = []
        self.name = ""

    def initialize_video_scroll(self, vid, names, keys):
        for i in names:
            self.dic[i] = []

        for i, j in zip(names, keys):
            self.n_dic[i] = j

        self.top_label = str(self.n_dic)[1:-1].replace("'", "")
        split = vid.split('.')
        vid_name = os.path.basename(split[0])
        cap = cv2.VideoCapture(vid)
        fps = cap.get(cv2.CAP_PROP_FPS)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1

        cv2.namedWindow(self.top_label, cv2.WINDOW_NORMAL)
        cv2.createTrackbar('pos', self.top_label, 0, length, self.onChange)
        self.onChange(0)

        while cap.isOpened():
            k = cv2.waitKey(0)
            self.handle_key_press(k, keys)

            if k == 27:
                for i in range(len(self.dic)):
                    if len(self.dic[names[i]]) % 2 != 0:
                        pos = cv2.getTrackbarPos('pos', self.top_label)
                        self.dic[list(self.dic)[i]].append(pos)
                return self.dic

        cap.release()
        cv2.destroyAllWindows()

    def onChange(self, trackbarValue):
        cap.set(cv2.CAP_PROP_POS_FRAMES, trackbarValue)
        _, img = cap.read()
        h, w, _ = img.shape

        if self.cnt == 1:
            n_img = cv2.putText(img, self.name, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1,
                                cv2.LINE_AA, False)
            cv2.imshow(self.top_label, n_img)

        if self.cnt == 0:
            cv2.imshow(self.top_label, img)

        if self.reset == 1:
            n_img = cv2.putText(img, 'reset', (w - 70, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                                (255, 255, 255), 1, cv2.LINE_AA, False)
            cv2.imshow(self.top_label, n_img)

        if self.show == 1:
            dic_temp = {}
            temp = list(self.dic.values())
            for i, j in zip(range(len(temp)), self.dic.keys()):
                l = temp[i][-2:]
                l.append(str(len(temp[i])))
                dic_temp[j] = l
            n_img = cv2.putText(img, str(dic_temp), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                                (255, 255, 255), 1, cv2.LINE_AA, False)
            cv2.imshow(self.top_label, n_img)

    def handle_key_press(self, key, keys):
        for i in range(len(keys)):
            if key == ord(keys[i]):
                if self.compare == [] or keys[i] == self.compare[0]:
                    self.compare.append(keys[i])
                    pos = cv2.getTrackbarPos('pos', self.top_label)
                    self.dic[list(self.dic)[i]].append(pos)
                    self.name = list(self.dic)[i]
                    l = len(list(self.dic.values())[i])

                    if l % 2 != 0:
                        self.cnt = 1

                    if l % 2 == 0:
                        self.cnt = 0
                        self.compare = []

                    self.onChange(pos)

        if key == 8:
            self.reset = 1
            pos = cv2.getTrackbarPos('pos', self.top_label)
            self.onChange(pos)
            if self.compare != []:
                self.compare = self.compare[:-1]
            i = self.getmax(self.dic)
            del self.dic[names[i]][-1]

            if self.cnt == 1:
                self.cnt = 0
            else:
                self.cnt = 1

            self.reset = 0

        if key == ord('p'):
            self.show = 1
            pos = cv2.getTrackbarPos('pos', self.top_label)
            self.onChange(pos)
            self.show = 0

    def getmax(self, data):
        m_list = []
        t = list(data.values())
        for i in t:
            if i != []:
                m_list.append(max(i))
            else:
                m_list.append(0)
        return m_list.index(max(m_list))


# Example Usage:
# video_scroll_obj = VideoScroll()
# video_scroll_obj.initialize_video_scroll('your_video.mp4', ['Object1', 'Object2'], ['a', 'b'])
