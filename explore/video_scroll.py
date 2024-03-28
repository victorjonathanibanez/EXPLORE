'''import cv2
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
'''

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QScrollBar
from PyQt5.QtGui import QPixmap, QImage
import cv2

class VideoLabelingGUI(QMainWindow):
    def __init__(self, video_path, key_dict):
        super().__init__()
        self.video_path = video_path
        self.key_dict = key_dict
        self.sequences = {}
        self.current_sequence = None
        self.frame_counter = 0
        self.cap = cv2.VideoCapture(self.video_path)

        self.setWindowTitle("Video Labeling Tool")
        self.setGeometry(100, 100, 800, 600)

        self.frame_label = QLabel(self)
        self.frame_label.setGeometry(50, 50, 700, 400)

        self.key_display = QLabel(self)
        self.key_display.setGeometry(50, 470, 200, 30)

        self.scrollbar = QScrollBar(self)
        self.scrollbar.setGeometry(50, 520, 700, 20)
        self.scrollbar.valueChanged.connect(self.on_scroll)

        self.submit_button = QPushButton('Submit', self)
        self.submit_button.setGeometry(50, 550, 100, 30)
        self.submit_button.clicked.connect(self.submit)

        self.update_frame()

    def on_scroll(self, value):
        self.frame_counter = value
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_counter)
        self.update_frame()

    def keyPressEvent(self, event):
        key = event.text()
        if key in self.key_dict:
            if self.current_sequence is None:
                self.current_sequence = [self.frame_counter]
                if self.key_display.text() != self.key_dict[key]:
                    self.key_display.setText(self.key_dict[key])
                else:
                    self.key_display.setText("")
            else:
                self.current_sequence.append(self.frame_counter)
        elif key == " " and self.current_sequence is not None:
            if len(self.current_sequence) > 1:
                sequence_key = self.key_display.text()
                if sequence_key in self.key_dict.values():
                    if sequence_key not in self.sequences:
                        self.sequences[sequence_key] = []
                    self.sequences[sequence_key].append((self.current_sequence[1], self.frame_counter))
            self.current_sequence = None
            self.key_display.setText("")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QPixmap.fromImage(QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888))
            self.frame_label.setPixmap(q_img)

    def submit(self):
        for key in self.sequences:
            if len(self.sequences[key]) == 0:
                del self.sequences[key]
        self.close()

def main():
    app = QApplication(sys.argv)
    video_path = "/Users/victor/Desktop/work/test/test_label_video.MP4"
    key_dict = {"a": "sequence_a", "b": "sequence_b"}  # Example key-value pairs
    gui = VideoLabelingGUI(video_path, key_dict)
    print(gui.sequences)  # You can access the labeled sequences from here
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

