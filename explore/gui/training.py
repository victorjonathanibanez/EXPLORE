from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class TrainingGUI:
    def __init__(self, master, on_close_callback=None):
        self.master = master
        self.on_close_callback = on_close_callback
        master.title("EXPLORE - Create a new project")

        # Variable to store the submitted data
        self.submitted_data = None

        # Labels
        Label(master, text="Project Name:").grid(row=0, column=0, sticky="e")
        Label(master, text="Video Length (min):").grid(row=1, column=0, sticky="e")
        Label(master, text="Choose Project Path:").grid(row=2, column=0, sticky="e")
        Label(master, text="Choose Videos Path:").grid(row=4, column=0, sticky="e")
        Label(master, text="").grid(row=5, column=0)  # Empty line
        Label(master, text="Length of Manual Scoring Video (min):").grid(row=7, column=0, sticky="e")
        Label(master, text="Objects:").grid(row=8, column=0, sticky="e")

        # Create Spinbox widgets for video length and manual scoring video length
        self.video_length_spinbox = Spinbox(master, from_=1, to=60)  # Example range from 1 to 60 minutes
        self.video_length_spinbox.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.manual_scoring_video_length_spinbox = Spinbox(master, from_=1, to=60)  # Example range from 1 to 60 minutes
        self.manual_scoring_video_length_spinbox.grid(row=7, column=1, pady=5, padx=10, sticky="w")

        # Entry fields
        self.project_name_entry = Entry(master)
        self.project_name_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        # Initial width for project path entry
        self.project_path_width = 20

        # Choose Project Path button
        self.selected_video_paths = []
        self.choose_path_button = Button(master, text="Select", command=self._choose_project_path)
        self.choose_path_button.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Choose Project Path button
        self.selected_project_paths = []
        self.choose_vid_path_button = Button(master, text="Select", command=self._choose_video_path)
        self.choose_vid_path_button.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        Label(master, text="").grid(row=5, column=1)  # Empty line

        # Objects label
        self.objects_label = Label(master, text="")
        self.objects_label.grid(row=8, column=1, pady=5, padx=10, sticky="w")

        # Add Object button
        self.add_object_button = Button(master, text="Add Object", command=self._add_object)
        self.add_object_button.grid(row=8, column=1, pady=5, padx=10, sticky="w")

        # Remove Object button (disabled initially)
        self.remove_object_button = Button(master, text="Remove Object", command=self._remove_object, state=DISABLED)
        self.remove_object_button.grid(row=8, column=2, pady=5, padx=10, sticky="e")

        # Submit button
        self.submit_button = Button(master, text="Submit", command=self._submit_and_close)
        self.submit_button.grid(row=11, column=0, columnspan=2, pady=(20, 5))

        # List to store dynamically added Entry widgets
        self.object_entries = []

    def _choose_project_path(self):
        # Remove any existing labels displaying project path
        existing_label = self.master.grid_slaves(row=3, column=1)
        if existing_label:
            existing_label[0].destroy()

        # Ask the user to select the project path
        project_path = filedialog.askdirectory()
        if project_path:
            # Store the selected project paths in the instance variable
            self.selected_project_paths = project_path
            # Display the path as a string below the 'Choose Project Path'
            Label(self.master, text=project_path).grid(row=3, column=1, columnspan=2, pady=5, padx=10, sticky="w")
            self.project_path_width = len(project_path) if len(project_path) > 20 else 20
            self.choose_path_button.grid(row=2, column=1, sticky="w", pady=5)
        else:
            self.choose_path_button.grid(row=2, column=1, sticky="w", pady=5)

    def _choose_video_path(self):
        # Remove any existing labels displaying video paths
        existing_labels = self.master.grid_slaves(row=5, column=1)
        for label in existing_labels:
            label.destroy()

        # Ask the user to select video paths
        video_paths = filedialog.askopenfilenames()
        if video_paths:
            # Store the selected video paths in the instance variable
            self.selected_video_paths = video_paths
            # Display the paths as a list below the 'Choose Videos Path'
            paths_text = "\n".join(video_paths)
            Label(self.master, text=paths_text).grid(row=5, column=1, columnspan=2, pady=5, padx=10, sticky="w")
            self.video_path_width = max(len(path) for path in video_paths) if video_paths else 20
            self.choose_vid_path_button.grid(row=4, column=1, sticky="w", pady=5)
        else:
            self.choose_vid_path_button.grid(row=4, column=1, sticky="w", pady=5)

    def _add_object(self):
        # Create labels for the first entry fields
        add_object_label = Label(self.master, text="Add object name:")
        add_object_label.grid(row=len(self.object_entries) + 9, column=0, padx=10, pady=5, sticky="e")

        add_key_label = Label(self.master, text="Add key: (a-z; 'p' reserved):")
        add_key_label.grid(row=len(self.object_entries) + 9, column=2, padx=10, pady=5, sticky="e")

        # Create Entry widgets for object and key
        object_entry = Entry(self.master, width=20)
        key_entry = Entry(self.master, width=5)

        # Grid layout for master (not the frame)
        object_entry.grid(row=len(self.object_entries) + 9, column=1, padx=10, pady=5, sticky="w")
        key_entry.grid(row=len(self.object_entries) + 9, column=3, padx=10, pady=5, sticky="w")

        # Append the Entry widgets to the object_entries list
        self.object_entries.append((add_object_label, add_key_label, object_entry, key_entry))

        # Enable the Remove Object button
        self.remove_object_button["state"] = NORMAL

        # Move the Submit button dynamically
        self.submit_button.grid(row=len(self.object_entries) + 9, column=0, columnspan=2, pady=(20, 5))

    def _remove_object(self):
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
                self.submit_button.grid(row=11, column=0, columnspan=2, pady=(20, 5))

    def _error_message(self):
        if self.master:
            error_window = Toplevel(self.master)
            error_window.title("Error")
            Label(error_window, text="Missing entries!").pack(padx=20, pady=20)
            Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)
            error_window.mainloop()
    
    def _duplicate_error_message(self):
        if self.master:
            error_window = Toplevel(self.master)
            error_window.title("Error")
            Label(error_window, text="Duplicate keyboard keys are not allowed!").pack(padx=20, pady=20)
            Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)
            error_window.mainloop()
        
    def _check_if_submitted_fields_contain_entries(self, entries_to_check):
        for value in entries_to_check.values():
            if isinstance(value, str) and len(value) == 0:
                self._error_message()
            elif isinstance(value, list) and len(value) == 0:
                self._error_message()

    def _check_if_object_key_pairs_exist(self, entries_to_check):
        for obj_name, obj_key in entries_to_check:
            if len(obj_name.strip()) == 0 or len(obj_key.strip()) == 0:
                self._error_message()    
        if not entries_to_check:
            self._error_message()
    
    def _check_unique_keys_and_values(self, data):
        unique_keys = set([i[0] for i in data])
        unique_values = set([i[1] for i in data])
        if len(unique_keys) < len(data) or len(unique_values) < len(data):
            self._duplicate_error_message()

    def _submit(self):

        # Retrieve values from entry fields
        project_name = self.project_name_entry.get()
        video_length = self.video_length_spinbox.get()
        manual_scoring_video_length = self.manual_scoring_video_length_spinbox.get()

        # Retrieve values from dynamically added objects
        objects_data = [(obj_entry.get(), key_entry.get()) for _, _, obj_entry, key_entry in self.object_entries]

    
        # Retrieve the project path from the file selection button
        project_path = self.selected_project_paths

        video_paths = self.selected_video_paths

        # Update the Objects label
        objects_text = "\n".join([f"{obj} - {key}" for obj, key in objects_data])
        self.objects_label.config(text=objects_text)

        # Create a dictionary with all the values
        data = {
            "Project Name": project_name,
            "Project Path": project_path,
            "Video Paths": video_paths,
            "Video Length": video_length,
            "Manual Scoring Video Length": manual_scoring_video_length
        }
        
        # checks for existing entries
        self._check_if_submitted_fields_contain_entries(data)
        self._check_if_object_key_pairs_exist(objects_data)
        self._check_unique_keys_and_values(objects_data)

        #data["Random Sampling"] = random_sampling
        data["Objects"] = objects_data

        # Store the data in the instance variable
        self.submitted_data = data


    def _submit_and_close(self):
        # Submit the data
        data = self._submit()
        
        # Close the window
        self.master.destroy()

        if self.on_close_callback:
            self.on_close_callback(self.submitted_data)

def on_window_close(data):
    print("Data from GUI:", data)
    return

if __name__ == "__main__":
    def on_window_close(data):
        print("Data from GUI:", data)

    root = Tk()
    my_gui = TrainingGUI(root, on_close_callback=on_window_close)
    root.mainloop()

