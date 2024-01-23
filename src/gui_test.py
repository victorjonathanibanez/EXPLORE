from tkinter import *
from tkinter import filedialog

class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Extended GUI")

        # Labels
        Label(master, text="Project Name:").grid(row=0, column=0, sticky="e")
        Label(master, text="Video Length (min):").grid(row=1, column=0, sticky="e")
        Label(master, text="Choose Project Path:").grid(row=2, column=0, sticky="e")
        Label(master, text="").grid(row=3, column=0)  # Empty line
        Label(master, text="Random Sampling:").grid(row=4, column=0, sticky="e")
        Label(master, text="Length of Manual Scoring Video (min):").grid(row=5, column=0, sticky="e")
        Label(master, text="Objects:").grid(row=6, column=0, sticky="e")

        # Entry fields
        self.project_name_entry = Entry(master)
        self.project_name_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        self.video_length_entry = Entry(master)
        self.video_length_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        # Initial width for project path entry
        self.project_path_width = 20

        # Choose Project Path button
        self.choose_path_button = Button(master, text="Choose", command=self.choose_project_path)
        self.choose_path_button.grid(row=2, column=1, sticky="w", pady=5)

        Label(master, text="").grid(row=3, column=1)  # Empty line

        self.random_sampling_var = IntVar()
        Radiobutton(master, text="Yes", variable=self.random_sampling_var, value=1).grid(row=4, column=1, padx=(0, 0))
        Radiobutton(master, text="No", variable=self.random_sampling_var, value=0).grid(row=4, column=1, padx=(0, 100))

        self.manual_scoring_entry = Entry(master)
        self.manual_scoring_entry.grid(row=5, column=1, pady=5, padx=10, sticky="w")

        # Objects label
        self.objects_label = Label(master, text="")
        self.objects_label.grid(row=6, column=1, pady=5, padx=10, sticky="w")

        # Add Object button
        self.add_object_button = Button(master, text="Add Object", command=self.add_object)
        self.add_object_button.grid(row=6, column=1, pady=5, padx=10, sticky="w")

        # Remove Object button (disabled initially)
        self.remove_object_button = Button(master, text="Remove Object", command=self.remove_object, state=DISABLED)
        self.remove_object_button.grid(row=6, column=1, pady=5, padx=10, sticky="e")

        # Submit button
        self.submit_button = Button(master, text="Submit", command=self.submit_and_close)
        self.submit_button.grid(row=9, column=0, columnspan=2, pady=(20, 5))

        # List to store dynamically added Entry widgets
        self.object_entries = []

    def choose_project_path(self):
        project_path = filedialog.askdirectory()
        if project_path:
            # Display the path as a string below the 'Choose Project Path'
            Label(self.master, text=project_path).grid(row=3, column=1, columnspan=2, pady=5, padx=10, sticky="w")
            self.project_path_width = len(project_path) if len(project_path) > 20 else 20
            self.choose_path_button.grid(row=2, column=1, sticky="w", pady=5)
        else:
            self.choose_path_button.grid(row=2, column=1, sticky="w", pady=5)

    def add_object(self):
        # Create labels for the first entry fields
        add_object_label = Label(self.master, text="Add object name:")
        add_object_label.grid(row=len(self.object_entries) + 7, column=0, padx=10, pady=5, sticky="e")

        add_key_label = Label(self.master, text="Add key: (a-z; 'p' reserved):")
        add_key_label.grid(row=len(self.object_entries) + 7, column=2, padx=10, pady=5, sticky="e")

        # Create Entry widgets for object and key
        object_entry = Entry(self.master, width=20)
        key_entry = Entry(self.master, width=5)

        # Grid layout for master (not the frame)
        object_entry.grid(row=len(self.object_entries) + 7, column=1, padx=10, pady=5, sticky="w")
        key_entry.grid(row=len(self.object_entries) + 7, column=3, padx=10, pady=5, sticky="w")

        # Append the Entry widgets to the object_entries list
        self.object_entries.append((add_object_label, add_key_label, object_entry, key_entry))

        # Enable the Remove Object button
        self.remove_object_button["state"] = NORMAL

        # Move the Submit button dynamically
        self.submit_button.grid(row=len(self.object_entries) + 9, column=0, columnspan=2, pady=(20, 5))

    def remove_object(self):
        if self.object_entries:
            # Remove the labels and Entry widgets from the master
            add_object_label, add_key_label, object_entry, key_entry = self.object_entries.pop()
            add_object_label.destroy()
            add_key_label.destroy()
            object_entry.destroy()
            key_entry.destroy()

            # Disable the Remove Object button if there are no more objects
            if not self.object_entries:
                self.remove_object_button["state"] = DISABLED

                # Move the Submit button back to the original position
                self.submit_button.grid(row=9, column=0, columnspan=2, pady=(20, 5))

    def submit_and_close(self):
        # Submit the data
        data = self.submit()

        # Close the window
        self.master.destroy()

    def submit(self):
        # Retrieve values from entry fields
        project_name = self.project_name_entry.get()
        video_length = self.video_length_entry.get()
        project_path = self.project_path_entry.get()
        random_sampling = bool(self.random_sampling_var.get())
        manual_scoring = self.manual_scoring_entry.get()

        # Retrieve values from dynamically added objects
        objects_data = [(obj_entry.get(), key_entry.get()) for _, _, obj_entry, key_entry in self.object_entries]

        # Update the Objects label
        objects_text = "\n".join([f"{obj} - {key}" for obj, key in objects_data])
        self.objects_label.config(text=objects_text)

        # Create a dictionary with all the values
        data = {
            "Project Name": project_name,
            "Video Length": video_length,
            "Project Path": project_path,
            "Random Sampling": random_sampling,
            "Manual Scoring Video Length": manual_scoring,
            "Objects": objects_data
        }

        # Print or process the dictionary as needed
        print(data)
        # Return the dictionary if needed
        return data

if __name__ == "__main__":
    root = Tk()
    my_gui = MyGUI(root)
    root.mainloop()
