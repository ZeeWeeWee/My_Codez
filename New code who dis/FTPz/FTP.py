import tkinter as tk
from ftplib import FTP

class FTPClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("FTP Client GUI")

        self.create_widgets()

    def create_widgets(self):
        self.server_label = tk.Label(self.master, text="Server:")
        self.server_label.pack(pady=5)
        self.server_entry = tk.Entry(self.master)
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

    def connect_to_ftp(self):
        server = self.server_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if server and username:
            try:
                ftp = FTP(server)
                ftp.login(username, password)

                # Now you are connected to the FTP server, you can perform operations here.

                print("Connected to FTP Server")
            except Exception as e:
                print(f"Error connecting to FTP Server: {e}")
        else:
            print("Please enter valid server and username.")

if __name__ == "__main__":
    root = tk.Tk()
    ftp_client_gui = FTPClientGUI(root)
    root.mainloop()
