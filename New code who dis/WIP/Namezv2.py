import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
from datetime import datetime

def list_files_and_folders(folder_path):
    try:
        file_names = []
        folder_names = []

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                file_names.append(item)
            elif os.path.isdir(item_path):
                folder_names.append(item)

        return file_names, folder_names
    except OSError as e:
        print(f"Error: {e}")
        return [], []

def export_to_txt(content, output_path):
    try:
        with open(output_path, 'w') as file:
            for line in content:
                file.write(line + '\n')

        print(f"Content exported to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

class FolderListApp:
     def __init__(self, root):
        self.root = root
        self.root.title("Namez v2")  # Set the application name to "Namez"
        self.root.geometry("640x480")  # Change the size of the window to 640x480

        self.folder_label = tk.Label(root, text="Folder Path:")
        self.folder_label.pack()

        self.folder_entry = tk.Entry(root)
        self.folder_entry.pack()

        self.output_label = tk.Label(root, text="Output Folder:")
        self.output_label.pack()

        self.output_entry = tk.Entry(root)
        self.output_entry.pack()

        self.output_file_label = tk.Label(root, text="Output File Name:")
        self.output_file_label.pack()

        self.output_file_entry = tk.Entry(root)
        self.output_file_entry.pack()

        self.date_format_label = tk.Label(root, text="Date Format (optional):")
        self.date_format_label.pack()

        self.date_format_entry = tk.Entry(root)
        self.date_format_entry.pack()

        self.date_format_info = tk.Label(root, text="If you enter the date format as -%Y%m%d-%H%M%S, the generated file names will include the date and time in the format like this: _files-20230809-143025.txt")
        self.date_format_info.pack()

        self.run_button = tk.Button(root, text="Generate List", command=self.generate_list)
        self.run_button.pack()

def generate_list(self):
        folder_path = self.folder_entry.get()
        output_location = self.output_entry.get()
        output_file_name = self.output_file_entry.get()
        date_format = self.date_format_entry.get()

        if not folder_path or not output_location or not output_file_name:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        output_files = []

        try:
            file_names, folder_names = list_files_and_folders(folder_path)

            if date_format:
                date_str = datetime.now().strftime(date_format)
                date_str = "_" + date_str
            else:
                date_str = ""

            file_output_path = os.path.join(output_location, output_file_name + "_files" + date_str + ".txt")
            folder_output_path = os.path.join(output_location, output_file_name + "_folders" + date_str + ".txt")

            export_to_txt(file_names, file_output_path)
            export_to_txt(folder_names, folder_output_path)

            log_content = [
                f"Folder Path: {folder_path}",
                f"Output Location: {output_location}",
                f"Output File Name: {output_file_name}",
                f"Date Format: {date_format}"
            ]
            
            log_path = os.path.join(output_location, output_file_name + "_user_inputs_log" + date_str + ".txt")
            export_to_txt(log_content, log_path)

            messagebox.showinfo("Success", "File list generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderListApp(root)
    root.mainloop()
