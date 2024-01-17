import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ftplib import FTP, error_perm
import configparser
import os
import threading

class ConfigHandler:
    def __init__(self, filename='config.ini'):
        self.config = configparser.ConfigParser()
        self.filename = filename

    def load_config(self):
        if os.path.exists(self.filename):
            self.config.read(self.filename)
            return dict(self.config['FTP'])
        return {}

    def save_config(self, server, username, password):
        self.config['FTP'] = {
            'server': server,
            'username': username,
            'password': password  # Caution: storing passwords in plain text
        }
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

class FTPClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("FTP Client GUI")

        # Styling configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 10), padding=5)
        self.style.configure('Treeview', rowheight=25)

        self.ftp = None
        self.current_directory = "/"
        self.config_handler = ConfigHandler()

        self.create_widgets()
        self.load_saved_config()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Server
        ttk.Label(main_frame, text="Server:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.server_entry = ttk.Entry(main_frame)
        self.server_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.server_entry.insert(0, "ftp.councilofheresy.com")

        # Username
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # Password
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        # Passive Mode Checkbox
        self.passive_mode_var = tk.IntVar()
        ttk.Checkbutton(main_frame, text="Use Passive Mode", variable=self.passive_mode_var).grid(row=3, column=0, columnspan=2, pady=5)

        # Connect Button
        self.connect_button = ttk.Button(main_frame, text="Connect to FTP Server", command=self.connect_to_ftp)
        self.connect_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Save Server Details Button
        self.save_button = ttk.Button(main_frame, text="Save Server Details", command=self.save_server_details)
        self.save_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Status Label
        self.status_label = ttk.Label(main_frame, text="", foreground="red")
        self.status_label.grid(row=6, column=0, columnspan=2)

    def load_saved_config(self):
        saved_config = self.config_handler.load_config()
        if saved_config:
            self.server_entry.insert(0, saved_config.get('server', ''))
            self.username_entry.insert(0, saved_config.get('username', ''))
            self.password_entry.insert(0, saved_config.get('password', ''))

    def save_server_details(self):
        server = self.server_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.config_handler.save_config(server, username, password)
        self.update_status("Server details saved.")

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

    def create_file_browser_window(self):
        # Hide the main window
        self.master.withdraw()

        self.file_browser_window = tk.Toplevel(self.master)
        self.file_browser_window.title("FTP File Browser")
        self.file_browser_window.protocol("WM_DELETE_WINDOW", self.on_file_browser_close)

        self.path_label = ttk.Label(self.file_browser_window, text="Current Path: /")
        self.path_label.pack(pady=5)

        self.file_tree = ttk.Treeview(self.file_browser_window, selectmode='extended', columns=("Name", "Size", "Last Modified", "Type"), show="headings")
        self.file_tree.column("Name", anchor=tk.W, width=250)
        self.file_tree.heading("Name", text="Name", anchor=tk.W)
        self.file_tree.column("Size", anchor=tk.CENTER, width=100)
        self.file_tree.heading("Size", text="Size (bytes)", anchor=tk.CENTER)
        self.file_tree.column("Last Modified", anchor=tk.CENTER, width=150)
        self.file_tree.heading("Last Modified", text="Last Modified", anchor=tk.CENTER)
        self.file_tree.column("Type", anchor=tk.CENTER, width=100)
        self.file_tree.heading("Type", text="Type", anchor=tk.CENTER)
        self.file_tree.pack(expand=tk.YES, fill=tk.BOTH)
        self.file_tree.bind("<Double-1>", self.on_tree_item_double_click)

        self.back_button = ttk.Button(self.file_browser_window, text="Back", command=self.go_back)
        self.back_button.pack(pady=5)

        self.download_button = ttk.Button(self.file_browser_window, text="Download Files", command=self.download_files)
        self.download_button.pack(pady=10)

        self.upload_button = ttk.Button(self.file_browser_window, text="Upload Files", command=self.upload_files)
        self.upload_button.pack(pady=10)

        self.disconnect_button = ttk.Button(self.file_browser_window, text="Disconnect", command=self.disconnect_from_ftp)
        self.disconnect_button.pack(pady=10)

    def on_file_browser_close(self):
        self.file_browser_window.destroy()
        self.master.deiconify()

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
                file_type = 'Directory' if file_info.startswith('d') else 'File'
                file_name = file_details[-1]
                file_size = file_details[4] if not file_type == 'Directory' else ''
                last_modified = " ".join(file_details[5:8])
                self.file_tree.insert("", "end", values=(file_name, file_size, last_modified, file_type))

    def download_files(self):
        selected_items = self.file_tree.selection()
        for item in selected_items:
            selected_file = self.file_tree.item(item)["values"][0]
            local_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")], initialfile=selected_file)
            
            if local_file_path:
                self.update_status(f"Downloading '{selected_file}'...")
                threading.Thread(target=self._download_thread, args=(selected_file, local_file_path)).start()

    def _download_thread(self, selected_file, local_file_path):
        try:
            with open(local_file_path, "wb") as local_file:
                self.ftp.retrbinary(f"RETR {selected_file}", local_file.write)
            self.update_status(f"File '{selected_file}' downloaded to '{local_file_path}'")
        except Exception as e:
            self.update_status(f"Error downloading file '{selected_file}': {e}")

    def upload_files(self):
        files_to_upload = filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])
        for file_path in files_to_upload:
            filename = os.path.basename(file_path)
            self.update_status(f"Uploading '{filename}'...")
            threading.Thread(target=self._upload_thread, args=(file_path,)).start()

    def _upload_thread(self, file_to_upload):
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

        if hasattr(self, 'file_browser_window'):
            self.file_browser_window.destroy()
            self.master.deiconify()

    def on_tree_item_double_click(self, event):
        selected_item = self.file_tree.selection()
        if selected_item:
            file_name = self.file_tree.item(selected_item)["values"][0]
            file_type = self.file_tree.item(selected_item)["values"][3]
            if file_type == 'Directory':
                try:
                    # Quote the directory name to handle spaces
                    quoted_file_name = f'"{file_name}"'
                    self.ftp.cwd(quoted_file_name)

                    # Update the current directory path
                    self.current_directory = self.ftp.pwd()
                    self.path_label.config(text=f"Current Path: {self.current_directory}")

                    # Update the file tree
                    self.update_file_tree()
                except Exception as e:
                    self.update_status(f"Error changing directory: {e}")


    def is_directory(self, file_name):
        try:
            self.ftp.cwd(file_name)
            self.ftp.cwd('..')
            return True
        except error_perm:
            return False

    def go_back(self):
        if self.current_directory != "/":
            # Change to the parent directory
            try:
                self.ftp.cwd('..')  # Go up one directory

                # Update the current directory path
                self.current_directory = self.ftp.pwd()
                self.path_label.config(text=f"Current Path: {self.current_directory}")

                # Update the file tree to show the contents of the new directory
                self.update_file_tree()
            except Exception as e:
                self.update_status(f"Error changing to parent directory: {e}")
        else:
            self.update_status("Already at the root directory.")

    def update_status(self, message):
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    ftp_client_gui = FTPClientGUI(root)
    root.mainloop()
