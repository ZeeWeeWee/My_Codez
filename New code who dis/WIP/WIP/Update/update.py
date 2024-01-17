import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ftplib import FTP
import os
import psutil
import time

# Predefined FTP server information
server_address = "councilofheresy.com"
username = "buttonz"
password = "bboey"
remote_folder = "/buttonz"
local_folder = 'c:\\buttonz'

def list_remote_files(ftp, folder):
    """Recursively list all files in the specified FTP folder and its subfolders."""
    file_list = []
    items = ftp.nlst(folder)

    for item in items:
        try:
            # Check if item is a directory
            if ftp.cwd(item):
                # If it's a directory, recursively list its contents
                file_list.extend(list_remote_files(ftp, item))
                ftp.cwd("..")  # Go back to the parent directory
        except:
            # If it's a file, add to the file list
            file_list.append(item)
    
    return file_list

def get_remote_file_size(ftp, filename):
    """Returns the size of the file on the FTP server."""
    ftp.voidcmd("TYPE I")  # Set to binary mode
    return ftp.size(filename)

def get_local_file_size(filepath):
    """Returns the size of the local file."""
    return os.path.getsize(filepath) if os.path.exists(filepath) else 0

def terminate_process(process_name):
    """Terminates processes with a given name."""
    for process in psutil.process_iter():
        try:
            pinfo = process.as_dict(attrs=['pid', 'name'])
            if pinfo['name'] == process_name:
                process.terminate()
        except psutil.NoSuchProcess:
            pass

def check_and_update_files():
    try:
        # Connect to the FTP server
        ftp = FTP(server_address)
        ftp.login(user=username, passwd=password)
        ftp.voidcmd("TYPE I")  # Set to binary mode
        
        remote_files = list_remote_files(ftp, remote_folder)
        
        files_to_update = []

        for remote_file in remote_files:
            local_path = os.path.join(local_folder, os.path.relpath(remote_file, remote_folder))
            
            # If the file doesn't exist in local folder, add to update list
            if not os.path.exists(local_path):
                files_to_update.append(remote_file)
                continue
            
            # If the file exists but sizes are different, add to update list
            remote_file_size = get_remote_file_size(ftp, remote_file)
            local_file_size = get_local_file_size(local_path)
            
            if remote_file_size != local_file_size:
                files_to_update.append(remote_file)
        
        progress_bar['maximum'] = len(files_to_update)
        progress_bar['value'] = 0

        for remote_file in files_to_update:
            local_path = os.path.join(local_folder, os.path.relpath(remote_file, remote_folder))
            
            # Ensure local directory exists
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Check if the file is running and close it
            terminate_process(os.path.basename(remote_file))
            time.sleep(1)  # Wait for a second to ensure the process has fully terminated

            # Download and overwrite the file in the local folder
            with open(local_path, 'wb') as file:
                ftp.retrbinary(f'RETR {remote_file}', file.write)
            
            progress_bar['value'] += 1
            window.update_idletasks()
        
        ftp.quit()
        
        if files_to_update:
            messagebox.showinfo("Update", f"Update completed. {len(files_to_update)} file(s) have been updated.")
        else:
            messagebox.showinfo("Update Check", "All files on your system are up-to-date.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# GUI code
window = tk.Tk()
window.title("Updater")
window.iconbitmap('c:\\Buttonz\\update.ico')
window.geometry("300x150")
main_frame = tk.Frame(window, bg="lightgrey")
main_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

label = tk.Label(main_frame, text="Checking and updating application files:", bg="lightgrey", font=("Arial", 12))
label.pack(pady=10)

progress_bar = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
progress_bar.pack(pady=10)

check_button = tk.Button(main_frame, text="Check & Update", command=check_and_update_files, bg="blue", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
check_button.pack(pady=10)

window.mainloop()
