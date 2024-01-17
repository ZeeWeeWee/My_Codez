import tkinter as tk
from tkinter import ttk, filedialog
from ftplib import FTP

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

        self.connect_button = tk.Button(self.master, text="Connect to FTP Server", command=self.connect_to_ftp)
        self.connect_button.pack(pady=10)

    def create_file_browser_window(self):
        file_browser_window = tk.Toplevel(self.master)
        file_browser_window.title("FTP File Browser")

        self.file_tree = ttk.Treeview(file_browser_window)
        self.file_tree["columns"] = ("Name", "Size")
        self.file_tree.column("#0", width=250, minwidth=250, stretch=tk.NO)
        self.file_tree.column("Name", anchor=tk.W, width=250, minwidth=150)
        self.file_tree.column("Size", anchor=tk.W, width=100, minwidth=50)
        self.file_tree.heading("#0", text="Path", anchor=tk.W)
        self.file_tree.heading("Name", text="Name", anchor=tk.W)
        self.file_tree.heading("Size", text="Size", anchor=tk.W)
        self.file_tree.pack(expand=tk.YES, fill=tk.BOTH)

        self.download_button = tk.Button(file_browser_window, text="Download File", command=self.download_file)
        self.download_button.pack(pady=10)

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
                self.ftp.set_pasv(False)  

                self.create_file_browser_window()

                self.update_file_tree()

                print("Connected to FTP Server")
            except Exception as e:
                print(f"Error connecting to FTP Server: {e}")
        else:
            print("Please enter valid server and username.")

    def update_file_tree(self):
        if self.ftp:
            self.file_tree.delete(*self.file_tree.get_children())
            files = self.ftp.nlst()

            for file in files:
                size = ""
                self.file_tree.insert("", "end", values=(file, size))

    def download_file(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            selected_file = self.file_tree.item(selected_item)["values"][0]
            local_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")])
            
            if local_file_path:
                with open(local_file_path, "wb") as local_file:
                    self.ftp.retrbinary(f"RETR {selected_file}", local_file.write)
                    print(f"File '{selected_file}' downloaded to '{local_file_path}'")

    def disconnect_from_ftp(self):
        if self.ftp:
            self.ftp.quit()
            print("Disconnected from FTP Server")

if __name__ == "__main__":
    root = tk.Tk()
    ftp_client_gui = FTPClientGUI(root)
    root.mainloop()
