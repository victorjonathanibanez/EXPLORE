from tkinter import *
import tkinter.filedialog as fd
import os

class GUITraining:
    def __init__(self):
        self.project_path = None
        self.entries = []
        self.var = None

    def create_gui(self):
        self.window = Tk()
        self.window.title('Create a new Project!')

        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        win_w = int(width / 2)
        win_h = int(height / 1.15)

        norm_w = 1280
        norm_f_size = 14
        f_size = round((norm_w * norm_f_size) / width)

        main_structure = {
            0.03: [['Label', [0.05, 'Project Name:']], ['Entry', [0.15, 30]]],
            0.08: [['Label', [0.05, 'Video Length (min):']], ['Entry', [0.15, 5]]],
            0.13: [['Label', [0.05, 'Choose Project Path:']], ['Button', [0.15, 'Browse', self.open_path]]],
            0.18: [['Label', [0.05, 'Random Sampling:']], ['Radiobutton', [0.15, 'Yes', 0.3, 'No']]],
            0.23: [['Label', [0.05, 'Length of Manual Scoring Video (min):']], ['Entry', [0.35, 5]]],
            0.28: [['Label', [0.05, 'Add Objects:']]],
            0.33: [['Label', [0.05, '1. Name:']], ['Entry', [0.15, 10]], ['Label', [0.35, 'Key:']], ['Entry', [0.45, 3]]],
            0.38: [['Label', [0.05, '2. Name:']], ['Entry', [0.15, 10]], ['Label', [0.35, 'Key:']], ['Entry', [0.45, 3]]],
            0.43: [['Label', [0.05, '3. Name:']], ['Entry', [0.15, 10]], ['Label', [0.35, 'Key:']], ['Entry', [0.45, 3]]],
            0.48: [['Label', [0.05, '4. Name:']], ['Entry', [0.15, 10]], ['Label', [0.35, 'Key:']], ['Entry', [0.45, 3]]],
            0.53: [['Label', [0.05, '5. Name:']], ['Entry', [0.15, 10]], ['Label', [0.35, 'Key:']], ['Entry', [0.45, 3]]],
            0.58: [['Label', [0.05, '6. Name:']], ['Entry', [0.15, 10]], ['Label', [0.35, 'Key:']], ['Entry', [0.45, 3]]],
            0.63: [['Button', [0.05, 'Submit']]],
        }

        self.call_dic(main_structure, self.window, f_size)

        self.window.geometry(str(win_w) + 'x' + str(win_h) + '+10+10')
        self.window.mainloop()

    def call_dic(self, dic, window, f_size):
        for key, value in dic.items():
            for i in range(len(value)):
                element_type, element_values = value[i]

                if element_type == 'Label':
                    self.create_label(window, *element_values, f_size)

                elif element_type == 'Entry':
                    self.create_entry(window, *element_values)

                elif element_type == 'Button':
                    if element_values[1] == 'path':
                        # If it's the 'path' button, call open_path method
                        self.create_button(window, *element_values, f_size, command=self.open_path)
                    elif element_values[1] == 'vid':
                        # If it's the 'vid' button, call open_vid method
                        self.create_button(window, *element_values, f_size, command=self.open_vid)
                    else:
                        # Handle other buttons as needed
                        self.create_button(window, *element_values, f_size)

                elif element_type == 'Radiobutton':
                    self.create_radiobutton(window, *element_values, f_size)

    def create_label(self, window, position, text, f_size):
        label = Label(window, text=text)
        label.grid(row=int(position * 100), column=0, sticky=W, padx=5, pady=5)
        label.config(font=("TkDefaultFont", f_size, "italic"))

    def create_entry(self, window, position, width):
        entry = Entry(window, bd=2, width=width)
        entry.grid(row=int(position * 100), column=1, sticky=W, padx=5, pady=5)
        self.entries.append(entry)

    def create_button(self, window, position, text, f_size, command=None):
        button = Button(window, text=text, command=lambda: command())
        button.place(x=int(window.winfo_screenwidth() * position), y=int(window.winfo_screenheight() * position))
        button.config(font=("TkDefaultFont", f_size, "italic"))

    def create_radiobutton(self, window, position, text1, position2, text2, f_size):
        global var

        var = IntVar()
        R1 = Radiobutton(window, text=text1, variable=var, value=1, command=self.handle_option_1)
        R1.grid(row=int(position * 100), column=3, sticky=W, padx=5, pady=5)
        R1.config(font=("TkDefaultFont", f_size, "italic"))

        R2 = Radiobutton(window, text=text2, variable=var, value=2, command=self.handle_option_2)
        R2.grid(row=int(position2 * 100), column=3, sticky=W, padx=5, pady=5)
        R2.config(font=("TkDefaultFont", f_size, "italic"))

    def open_path(self):
        project_path = fd.askdirectory()
        self.create_label(self.window, 0.13, project_path.ljust(1000), 14)
        self.project_path = project_path

    def handle_option_1(self):
        print("Handling option 1")

    def handle_option_2(self):
        print("Handling option 2")

if __name__ == "__main__":
    gui_training = GUITraining()
    gui_training.create_gui()
