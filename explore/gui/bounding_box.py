import cv2
import tkinter as tk
from tkinter import messagebox
from collections import OrderedDict
from PIL import Image, ImageTk

class BoundingBoxGUI:
    def __init__(self, video_path, object_list):
        self.video_path = video_path
        self.object_list = object_list
        self.object_list.insert(0,'background')
        self.current_object_index = 0
        self.bounding_boxes = OrderedDict()

        self.root = tk.Tk()
        self.root.title("BoundingBoxGUI")

        self.cap = cv2.VideoCapture(self.video_path)
        self.frame = self.get_frame()
        
        self.canvas = tk.Canvas(self.root, width=self.frame.shape[1], height=self.frame.shape[0])
        self.canvas.pack()

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear)
        self.clear_button.pack(side=tk.LEFT)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(side=tk.RIGHT)
        
        self.label = tk.Label(self.root, text="Draw bounding box around: {}".format(self.object_list[0]))
        self.label.pack()

        self.root.bind("<ButtonPress-1>", self.start_box)
        self.root.bind("<B1-Motion>", self.draw_box)

        self.draw_frame()
        self.root.mainloop()

    def get_bounding_boxes(self):
        return self.bounding_boxes

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            messagebox.showerror("Error", "Video cannot be read.")
            self.root.destroy()

    def draw_frame(self):
        self.photo = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.photo = Image.fromarray(self.photo)
        self.photo = ImageTk.PhotoImage(self.photo)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def start_box(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="green")

    def draw_box(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        self.bounding_boxes[self.object_list[self.current_object_index]] = (self.start_x, self.start_y, event.x, event.y)

    def clear(self):
        self.start_x, self.start_y = None, None
        self.canvas.delete(self.rect)
        self.draw_frame()
        self.bounding_boxes.pop(self.object_list[self.current_object_index])

    def submit(self):
        if len(self.bounding_boxes) != 0 and len(self.bounding_boxes) > self.current_object_index:
            self.draw_frame() 
            self.current_object_index += 1

            if self.current_object_index < len(self.object_list):
                next_object = self.object_list[self.current_object_index]
                self.label.config(text="Draw bounding box around: {}".format(next_object))
                self.start_x, self.start_y = None, None
            else:
                self.cap.release()
                self.root.destroy()
        else:
            messagebox.showinfo("Information", "Please draw a bounding box before submitting.")

if __name__ == "__main__":
    video_path = "/Volumes/VERBATIM_HD/NOR/same_object_30092020/1-converted.avi"
    object_list = ["object1", "object2"]

    gui = BoundingBoxGUI(video_path, object_list)
    bounding_boxes = gui.get_bounding_boxes()
    print("Bounding boxes:", bounding_boxes)


