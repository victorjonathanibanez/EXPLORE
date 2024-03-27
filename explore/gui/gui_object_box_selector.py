import cv2
import tkinter as tk
from tkinter import messagebox
from collections import OrderedDict
from PIL import Image, ImageTk

class BoundingBoxGUI:
    def __init__(self, video_path, object_dict):
        self.video_path = video_path
        self.object_dict = object_dict
        self.current_object_index = 0
        self.bounding_boxes = OrderedDict()

        self.root = tk.Tk()
        self.root.title("BoundingBoxGUI")

        self.cap = cv2.VideoCapture(self.video_path)
        self.frame = self.get_frame()
        
        self.canvas = tk.Canvas(self.root, width=self.frame.shape[0], height=self.frame.shape[1])
        self.canvas.pack()

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear)
        self.clear_button.pack(side=tk.LEFT)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(side=tk.RIGHT)

        self.label = tk.Label(self.root, text="Draw bounding box around: {}".format(list(self.object_dict.keys())[0]))
        self.label.pack()

        self.root.bind("<ButtonPress-1>", self.start_box)
        self.root.bind("<B1-Motion>", self.draw_box)

        self.draw_frame()
        self.root.mainloop()

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            messagebox.showerror("Error", "Video cannot be read.")
            self.root.destroy()

    def draw_frame(self):
        self.photo = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)  # Convert frame to BGR format
        self.photo = Image.fromarray(self.photo)  # Convert BGR image to PIL Image
        self.photo = ImageTk.PhotoImage(self.photo)  # Convert PIL Image to PhotoImage
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def start_box(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="green")

    def draw_box(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def clear(self):
        self.canvas.delete(self.rect)
        self.clear_current_bounding_box()
        self.draw_frame() 

    def submit(self):
        if self.start_x is not None and self.start_y is not None:
            self.bounding_boxes[self.current_object_index] = (self.start_x, self.start_y, self.canvas.coords(self.rect)[2], self.canvas.coords(self.rect)[3])
            self.clear_current_bounding_box()
            self.draw_frame()

            self.current_object_index += 1

            if self.current_object_index < len(self.object_dict):
                next_object = list(self.object_dict.keys())[self.current_object_index]
                self.label.config(text="Draw bounding box around: {}".format(next_object))
            else:
                self.cap.release()
                self.root.destroy()
                print("Bounding boxes:", self.bounding_boxes)
        else:
            messagebox.showinfo("Information", "Please draw a bounding box before submitting.")

    def clear_current_bounding_box(self):
        self.start_x = None
        self.start_y = None
        self.canvas.delete(self.rect)

if __name__ == "__main__":
    video_path = "/Users/victor/Desktop/work/Masterarbeit/vids/new_analysis_deep_learning.mp4"  # Provide path to your video
    object_dict = {"background": "b", "object1": "a", "object2": "c"}  # Example object dictionary

    BoundingBoxGUI(video_path, object_dict)
