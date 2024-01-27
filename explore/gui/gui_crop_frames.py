import cv2
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

class ObjectSelector:
    def __init__(self):
        self.image = None
        self.ref_point = []
        self.crop = False
        self.v1 = IntVar()
        self.v2 = IntVar()
        self.v3 = IntVar()
        self.v4 = IntVar()
        self.root = None

    def grep_frame(self, video):
        vidcap = cv2.VideoCapture(video)
        success, image = vidcap.read()
        count = 1

        while success:
            if count == 50:
                return image
                break

            success, image = vidcap.read()
            count += 1

    def shape_selection(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ref_point = [(x, y)]
        elif event == cv2.EVENT_LBUTTONUP:
            self.ref_point.append((x, y))
            cv2.rectangle(self.image, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
            cv2.imshow("draw rectangle around surface / 'r' for again / 'c' for crop", self.image)

    def draw_grid(self, h, w):
        b, g, r = cv2.split(self.image)
        img = cv2.merge((r, g, b))

        self.root = Tk()

        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)

        canvas = Canvas(self.root, width=w, height=h)
        canvas.pack()
        canvas.create_image(w, h, image=imgtk, anchor='se')

        quit_button = Button(self.root, text="Save", command=self.submit, anchor='w', width=4)
        quit_button_window = canvas.create_window(10, 10, anchor='nw', window=quit_button)

        # get values
        C1 = Checkbutton(self.root, text="", variable=self.v1)
        C2 = Checkbutton(self.root, text="", variable=self.v2)
        C3 = Checkbutton(self.root, text="", variable=self.v3)
        C4 = Checkbutton(self.root, text="", variable=self.v4)

        C1.place(x=int(w/5), y=int(h/4))
        C2.place(x=int(w/5), y=int(h/4)*3)
        C3.place(x=int(w/5)*3, y=int(h/4))
        C4.place(x=int(w/5)*3, y=int(h/4)*3)

        self.root.title('Select your objects')
        self.root.mainloop()

    def submit(self):
        self.s1 = self.v1.get()
        self.s2 = self.v2.get()
        self.s3 = self.v3.get()
        self.s4 = self.v4.get()
        self.root.destroy()

    def main(self, video):
        self.image = self.grep_frame(video)
        self.ref_point = []
        self.crop = False

        clone = self.image.copy()
        cv2.namedWindow("draw rectangle around surface / 'r' for again / 'c' for crop", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("draw rectangle around surface / 'r' for again / 'c' for crop", self.shape_selection)
        cv2.startWindowThread()

        while True:
            cv2.imshow("draw rectangle around surface / 'r' for again / 'c' for crop", self.image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):
                self.image = clone.copy()
            elif key == ord("c"):
                break

        if len(self.ref_point) == 2:
            crop_img = clone[self.ref_point[0][1]:self.ref_point[1][1], self.ref_point[0][0]:self.ref_point[1][0]]
            h, w, _ = crop_img.shape
            self.draw_grid(h, w)

        cv2.destroyAllWindows()

        return self.ref_point  # self.s1, self.s2, self.s3, self.s4,
