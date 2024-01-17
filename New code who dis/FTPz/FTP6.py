import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ftplib import FTP, error_perm
import os
import threading

class FTPClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("FTP Client GUI")

        self.ftp = None
        self.current_directory = "/"
        
        self.create_widgets()

    def create_widgets(self):
        self.server_label = tk.Label(self.master, text="Server:")
        self.server_label.pack(pady=5)
        default_server_value = "ftp.councilofheresy.com"        
        self.server_entry = tk.Entry(self.master)
        self.server_entry.insert(0, default_server_value)
        self.server_entry.pack(pady=5)

        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack(pady=5)

        self.passive_mode_var = tk.IntVar()
        self.passive_mode_checkbox = tk.Checkbutton(self.master, text="Use Passive Mode", variable=self.passive_mode_var)
        self.passive_mode_checkbox.pack(pady=5)

        self.connect_button = tk.Button(self.master, text="Connect to FTP Server", command=self.connect_to_ftp)
        self.connect_button.pack(pady=10)

        self.status_label = tk.Label(self.master, text="", fg="red")
        self.status_label.pack(pady=5)

    def create_file_browser_window(self):
        file_browser_window = tk.Toplevel(self.master)
        file_browser_window.title("FTP File Browser")

        self.file_tree = ttk.Treeview(file_browser_window, columns=("Name", "Size", "Last Modified"), show="headings")
        self.file_tree.column("Name", anchor=tk.W, width=250)
        self.file_tree.heading("Name", text="Name", anchor=tk.W)
        self.file_tree.column("Size", anchor=tk.CENTER, width=100)
        self.file_tree.heading("Size", text="Size (bytes)", anchor=tk.CENTER)
        self.file_tree.column("Last Modified", anchor=tk.CENTER, width=150)
        self.file_tree.heading("Last Modified", text="Last Modified", anchor=tk.CENTER)
        self.file_tree.pack(expand=tk.YES, fill=tk.BOTH)

        self.download_button = tk.Button(file_browser_window, text="Download File", command=lambda: threading.Thread(target=self.download_file).start())
        self.download_button.pack(pady=10)

        self.upload_button = tk.Button(file_browser_window, text="Upload File", command=lambda: threading.Thread(target=self.upload_file).start())
        self.upload_button.pack(pady=10)

        self.disconnect_button = tk.Button(file_browser_window, text="Disconnect", command=self.disconnect_from_ftp)
        self.disconnect_button.pack(pady=10)

    def connect_to_ftp(self):
        server = self.server_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if server and username:
            try:
                self.ftp = FTP(server)
                self.ftp.login(username, password)
                if self.passive_mode_var.get():
                    self.ftp.set_pasv(True)
                else:
                    self.ftp.set_pasv(False)

                self.create_file_browser_window()
                self.update_file_tree()

                self.update_status("Connected to FTP Server")
            except Exception as e:
                self.update_status(f"Error connecting to FTP Server: {e}")
        else:
            self.update_status("Please enter a valid server and username.")

    def update_file_tree(self):
        if self.ftp:
            self.file_tree.delete(*self.file_tree.get_children())
            files = []
            try:
                self.ftp.retrlines('LIST', files.append)
            except error_perm as e:
                self.update_status(f"Error listing directory: {e}")
                return

            for file_info in files:
                file_details = file_info.split()
                file_name = file_details[-1]
                file_size = file_details[4]
                last_modified = " ".join(file_details[5:8])
                self.file_tree.insert("", "end", values=(file_name, file_size, last_modified))

    def download_file(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            selected_file = self.file_tree.item(selected_item)["values"][0]
            # Use the selected file name as the initial file name in the save dialog
            local_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")], initialfile=selected_file)
        
            if local_file_path:
                try:
                    with open(local_file_path, "wb") as local_file:
                        self.ftp.retrbinary(f"RETR {selected_file}", local_file.write)
                    self.update_status(f"File '{selected_file}' downloaded to '{local_file_path}'")
                except Exception as e:
                    self.update_status(f"Error downloading file '{selected_file}': {e}")

    def upload_file(self):
        file_to_upload = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])

        if file_to_upload:
            try:
                with open(file_to_upload, 'rb') as local_file:
                    filename = os.path.basename(file_to_upload)
                    self.ftp.storbinary(f"STOR {filename}", local_file)
                    self.update_status(f"File '{filename}' uploaded successfully")
                    self.update_file_tree()
            except Exception as e:
                self.update_status(f"Error uploading file '{file_to_upload}': {e}")

    def disconnect_from_ftp(self):
        if self.ftp:
            try:
                self.ftp.quit()
                self.update_status("Disconnected from FTP Server")
            except Exception as e:
                self.update_status(f"Error disconnecting from FTP Server: {e}")

    def update_status(self, message):
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    ftp_client_gui = FTPClientGUI(root)
    root.mainloop()
