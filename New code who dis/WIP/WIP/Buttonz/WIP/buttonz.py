import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import getpass
import platform
import subprocess
import psutil
import GPUtil
import cpuinfo
import random
from PIL import Image, ImageTk
import pygame
import pygame.mixer
import ctypes
import shutil
import sys
import keyboard
import webbrowser
#import time
import datetime
import json

# Define the is_admin() function
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Initialize pygame
pygame.mixer.init()

# Initialize night mode state
is_night_mode = False

# Get the username and AppData path
username = getpass.getuser()
appdata_path = os.path.join("C:\\Users", username, "AppData")

# Get the Documents folder path
documents_path = os.path.join("C:\\Users", username, "Documents")

# Convert bytes to megabytes
def bytes_to_megabytes(bytes_value):
    return bytes_value / (1024 * 1024)

# Function to get physical drive name based on drive letter
def get_physical_drive_name(drive_letter):
    drive_name = drive_letter
    try:
        partitions = psutil.disk_partitions()
        for partition in partitions:
            if partition.device == drive_letter:
                drive_name = partition.mountpoint
    except Exception as e:
        print(f"Error getting physical drive name: {e}")
    return drive_name

#-------------------------------------------------------------------------------------------------------------------------------------

def toggle_night_mode():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    global night_mode

    if night_mode:
        # Switch to day mode (original button colors)
        for button in all_buttons:
            button.config(bg="SystemButtonFace", fg="black")
        night_mode = False
    else:
        # Switch to night mode (black buttons with white text)
        for button in all_buttons:
            button.config(bg="black", fg="white")
        night_mode = True

#--------------------------------------------------------------------------------------------------------------------------------------

night_mode = False

def grab_system_specs():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    system_info = platform.uname()

    # Get detailed CPU information using cpuinfo library
    cpu_info_data = cpuinfo.get_cpu_info()
    processor = cpu_info_data["brand_raw"] if "brand_raw" in cpu_info_data else "Unknown CPU"

    specs = f"System Specs:\n\n" \
            f"System: {system_info.system}\n" \
            f"Node Name: {system_info.node}\n" \
            f"Release: {system_info.release}\n" \
            f"Version: {system_info.version}\n" \
            f"Machine: {system_info.machine}\n" \
            f"Processor: {processor}"

    # Get memory information
    memory = psutil.virtual_memory()
    specs += f"\n\nMemory:\nTotal Memory: {bytes_to_megabytes(memory.total):.2f} MB\nUsed Memory: {bytes_to_megabytes(memory.used):.2f} MB\nFree Memory: {bytes_to_megabytes(memory.free):.2f} MB"

    # Get storage information
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_usage = psutil.disk_usage(partition.mountpoint)
        drive_name = get_physical_drive_name(partition.device)
        specs += f"\n\nStorage ({drive_name}):\nTotal Space: {bytes_to_megabytes(partition_usage.total):.2f} MB\nUsed Space: {bytes_to_megabytes(partition_usage.used):.2f} MB\nFree Space: {bytes_to_megabytes(partition_usage.free):.2f} MB"

    # Get GPU information
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            for idx, gpu in enumerate(gpus):
                specs += f"\n\nGPU {idx + 1}:\nName: {gpu.name}\nDriver: {gpu.driver}\nMemory Total: {gpu.memoryTotal:.2f} MB\nMemory Free: {gpu.memoryFree:.2f} MB\nMemory Used: {gpu.memoryUsed:.2f} MB"
        else:
            specs += "\n\nNo GPU installed."
    except Exception as e:
        print(f"GPU retrieval error: {e}")
        specs += "\n\nError retrieving GPU information."

    # Get IP configuration (ipconfig)
    try:
        ipconfig_result = subprocess.run(['ipconfig', '/all'], stdout=subprocess.PIPE, text=True)
        ipconfig_output = ipconfig_result.stdout
        specs += f"\n\nIP Configuration:\n{ipconfig_output}"
    except Exception as e:
        print(f"IP configuration error: {e}")
        specs += "\n\nError retrieving IP configuration."

    # Create a text file in the AppData directory
    txt_file_path = os.path.join(appdata_path, "system_specs.txt")
    with open(txt_file_path, 'w') as file:
        file.write(specs)

    # Open the text file with default text editor
    subprocess.Popen(['notepad.exe', txt_file_path])

#--------------------------------------------------------------------------------------------

def open_c_drive():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    os.startfile("C:")

# Function to run a custom executable
def run_custom_exe():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_path = 'C:\\Buttonz\\REemv_Setup.exe'
    os.startfile(exe_path)

# Function to run POS DOS
def run_posdos():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_posdos = 'C:\\Buttonz\\POS DOS'
    os.startfile(exe_posdos)

# Function to run searchz
def run_searchz():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    searchz_exe = 'C:\\Buttonz\\searchz.exe'
    os.startfile(searchz_exe)

# Function to run a danger noodle game
def run_custom_exe_2():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_path_2 = 'C:\\Buttonz\\danger_noodle.exe'
    os.startfile(exe_path_2)
    
# Function to run a ChatGPT
def run_custom_exe_3():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_path_3 = 'C:\\Buttonz\\CGBT\\ChatGPT.exe'
    os.startfile(exe_path_3)

# Function to run a Read Only
def run_custom_exe4():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_path = 'C:\\Buttonz\\clear_read_only.exe'
    os.startfile(exe_path)

# Function to run a Epson OPOS
def run_custom_exe5():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_path = 'C:\\Program Files (x86)\\OPOS\\Epson2\\StartPOS.exe'
    os.startfile(exe_path)

# Function to open AppData folder
def open_appdata_folder():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    os.startfile(appdata_path)

# Function to run the specified bat file
def run_custom_bat():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    bat_path = 'C:\\Buttonz\\V8toE_1.7.bat'
    subprocess.Popen(['cmd.exe', '/C', bat_path], shell=True)

# Function to open and edit a batch file, then run it
def edit_and_run_batch():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    batch_path = 'C:\\Buttonz\\updbal.bat'
    try:
        subprocess.Popen(['notepad.exe', batch_path]).wait()
        subprocess.Popen(['cmd.exe', '/C', batch_path], shell=True)
    except Exception as e:
        print(f"Error editing and running batch file: {e}")

# Function to run MX9Reboot.exe
def run_mx9_reboot():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_path = 'C:\\Buttonz\\MX9Reboot.exe'
    os.startfile(exe_path)

# Function to run Dual Test
def run_dualtest():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_path = 'C:\\Program Files (x86)\\DLSOPOS\\Driver\\DualTest.exe'
    os.startfile(exe_path)

# Function to run Pinpadinfo.exe
def run_pinpad_info():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_path = 'C:\\Buttonz\\Pinpadinfo.exe'
    os.startfile(exe_path)

# Function to run update.exe
def update():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_path = 'C:\\Buttonz\\update.exe'
    os.startfile(exe_path)

# Function to run update.exe
def extenz():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_path = 'C:\\Buttonz\\extenz.exe'
    os.startfile(exe_path)

# Function to run update_update.exe
def update2():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    exe_path = 'C:\\Buttonz\\update_update.exe'
    os.startfile(exe_path)

# Function to randomly choose a background audio file
def choose_random_background():
    backgrounds = [
        "C:\\Buttonz\\background1.mp3",
        "C:\\Buttonz\\background2.mp3",
        "C:\\Buttonz\\background3.mp3",
    ]
    return random.choice(backgrounds)

# Function to set the volume
def set_volume(volume):
    pygame.mixer.music.set_volume(int(volume) / 0.3)

# Function to toggle mute state
def toggle_mute():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    global is_muted
    is_muted = not is_muted
    if is_muted:
        pygame.mixer.music.set_volume(0.3)
        mute_button.config(text="Adjusted")
    else:
        pygame.mixer.music.set_volume(0.2)  # Set desired volume level (e.g., 0.5 for 50%)
        mute_button.config(text="Adjusted")

# Initialize mute state
is_muted = False

# Function to play or pause background music
current_song = None
song_position = 0

def toggle_music():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    global current_song, song_position

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        play_pause_button.config(text="Play Music")
        song_position = pygame.mixer.music.get_pos()  # Store the current position of the song
    else:
        if current_song is None:
            current_song = choose_random_background()
        if song_position > 0:
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play(-1, start=song_position / 1000)  # Resume from the stored position
        else:
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play(-1)
        play_pause_button.config(text="Pause Music")

# Function to change the background music
def change_background_music():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    global current_song, song_position  # Add this line to access the global variables
    pygame.mixer.music.stop()
    current_song = choose_random_background()  # Change the current song
    song_position = 0  # Reset the song position
    toggle_music()

# Play the background music
song_path = choose_random_background()
pygame.mixer.music.load(song_path)
#pygame.mixer.music.play(-1)  # Loop the song indefinitely

def edit_and_run_mx9_upgrade():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    mx9_ini_path = 'C:\\Buttonz\\MX9UPG\\MX9.ini'
    up_mx_bat_path = 'C:\\Buttonz\\MX9UPG\\UP-MX F1 Run as Admin.bat'
    mx9_final_path = 'C:\\MX9UPG\\MX9.ini'
    mx9_temp_dir = 'C:\\MX9UPG\\temp'
    
    # Source and destination paths
    source_path = 'C:\\Buttonz\\MX9UPG'
    destination_path = 'C:\\MX9UPG'

    # Copy the folder if it doesn't exist at the destination
    if not os.path.exists(destination_path):
        try:
            shutil.copytree(source_path, destination_path)
            print("MX9UPG folder copied successfully.")
        except Exception as e:
            print(f"Error copying MX9UPG folder: {e}")
    else:
        print("MX9UPG folder already exists at the destination.")
    
    try:
        
        # Open MX9.ini in Notepad
        subprocess.Popen(['notepad.exe', mx9_ini_path]).wait()

        # Create the temp directory if it doesn't exist
        if not os.path.exists(mx9_temp_dir):
            os.makedirs(mx9_temp_dir)

        # Save the edited MX9.ini file to a temporary location
        mx9_ini_temp_path = os.path.join(mx9_temp_dir, 'MX9_temp.ini')
        shutil.copy(mx9_ini_path, mx9_ini_temp_path)
        
        # Move the edited MX9_temp.ini back to the original location
        shutil.move(mx9_ini_temp_path, mx9_final_path)

        # Create a pop-up window to ask if the user wants to reload the pin pad
        user_input = messagebox.askquestion("Reload Pin Pad", "Would you like to reload the Pin pad now?")
        if user_input == "yes":
            # Run UP-MX F1 Run as Admin.bat with elevated privileges if not already admin
            if not is_admin():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", 'cmd.exe', f'/C "{up_mx_bat_path}"', None, 1)
            else:
                subprocess.Popen(['cmd.exe', '/C', up_mx_bat_path], shell=True)
        else:
            print("Pin pad reload canceled.")

    except Exception as e:
        print(f"Error editing and running MX9 upgrade: {e}")

# Define the path for the log file
log_file_path = os.path.join("C:\\Buttonz", "program_log.txt")

# Ensure the directory exists, create it if not
log_directory = os.path.dirname(log_file_path)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

#-------------------------------------------------------------------------------------------------------

def set_dns_settings(dns_servers, interface_name):
    try:
        dns_string = ','.join(dns_servers)
        args = ['netsh', 'interface', 'ipv4', 'set', 'dns', f'name="{interface_name}"', 'static', dns_string]
        ctypes.windll.shell32.ShellExecuteW(None, "runas", " ".join(args), None, None, 1)
        messagebox.showinfo("Set DNS", "DNS settings updated successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Error updating DNS settings.")

def set_network_ip(ip_address, subnet_mask, default_gateway, interface_name):
    try:
        command = f'netsh interface ip set address name="{interface_name}" static {ip_address} {subnet_mask} {default_gateway}'
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/C {command}", None, 1)
        messagebox.showinfo("Set IP", "IP address, subnet mask, and default gateway set successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Error setting IP address, subnet mask, or default gateway.")

def add_secondary_ip(ip_address, subnet_mask, interface_name):
    try:
        args = ['netsh', 'interface', 'ipv4', 'add', 'address', f'name="{interface_name}"', ip_address, subnet_mask]
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Error adding secondary IP address.")

def set_pos1_ip_and_dns():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    primary_ip_address = "192.168.9.11"   # Replace with the desired primary IP address
    secondary_ip_address = "192.168.1.111"  # Replace with the desired secondary IP address
    subnet_mask = "255.255.255.0"  # Replace with the desired subnet mask
    #default_gateway = "192.168.1.1"  # Replace with the desired default gateway
    dns_servers = "8.8.8.8"  # Replace with the desired DNS servers

    # Get the interface name
    active_interface = psutil.net_if_stats().keys()
    interface_name = next(iter(active_interface), "Local Area Connection")

    # Get user input for DNS servers
    default_gateway = simpledialog.askstring("Default Gateway", "Enter Your Default Gateway:")

    if default_gateway is None:
        return  # User canceled the input

    default_gateway = f'"{default_gateway}"'


    # Confirmation message box
    confirm_message = f"You are about to set the following settings for '{interface_name}':\n\n" \
                      f"Primary IP Address: {primary_ip_address}\n" \
                      f"Secondary IP Address: {secondary_ip_address}\n" \
                      f"Subnet Mask: {subnet_mask}\n" \
                      f"Default Gateway: {default_gateway}\n" \
                      f"DNS Servers: {', '.join(dns_servers)}\n\n" \
                      f"Do you want to continue?"

    if messagebox.askyesno("Confirm Changes", confirm_message):
        set_network_ip(primary_ip_address, subnet_mask, default_gateway, interface_name)
        add_secondary_ip(secondary_ip_address, subnet_mask, interface_name)
        set_dns_settings(dns_servers, interface_name)
        messagebox.showinfo("Set POS1 IP and DNS", "POS1 IP addresses and DNS settings set successfully.")
    else:
        messagebox.showinfo("Set POS1 IP and DNS", "Operation canceled.")

def set_pos2_ip_and_dns():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    primary_ip_address = "192.168.9.12"   # Replace with the desired primary IP address for POS2
    secondary_ip_address = "192.168.1.112"  # Replace with the desired secondary IP address for POS2
    subnet_mask = "255.255.255.0"  # Replace with the desired subnet mask
    #default_gateway = "192.168.1.1"  # Replace with the desired default gateway
    dns_servers = "8.8.8.8"  # Replace with the desired DNS servers

    # Get the interface name
    active_interface = psutil.net_if_stats().keys()
    interface_name = next(iter(active_interface), "Local Area Connection")

    # Get user input for DNS servers
    default_gateway = simpledialog.askstring("Default Gateway", "Enter Your Default Gateway:")

    if default_gateway is None:
        return  # User canceled the input

    default_gateway = f'"{default_gateway}"'

    # Confirmation message box
    confirm_message = f"You are about to set the following settings for '{interface_name}':\n\n" \
                      f"Primary IP Address: {primary_ip_address}\n" \
                      f"Secondary IP Address: {secondary_ip_address}\n" \
                      f"Subnet Mask: {subnet_mask}\n" \
                      f"Default Gateway: {default_gateway}\n" \
                      f"DNS Servers: {', '.join(dns_servers)}\n\n" \
                      f"Do you want to continue?"

    if messagebox.askyesno("Confirm Changes", confirm_message):
        set_network_ip(primary_ip_address, subnet_mask, default_gateway, interface_name)
        add_secondary_ip(secondary_ip_address, subnet_mask, interface_name)
        set_dns_settings(dns_servers, interface_name)
        messagebox.showinfo("Set POS2 IP and DNS", "POS2 IP addresses and DNS settings set successfully.")
    else:
        messagebox.showinfo("Set POS2 IP and DNS", "Operation canceled.")

def set_pos3_ip_and_dns():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    primary_ip_address = "192.168.9.13"   # Replace with the desired primary IP address for POS3
    secondary_ip_address = "192.168.1.113"  # Replace with the desired secondary IP address for POS3
    subnet_mask = "255.255.255.0"  # Replace with the desired subnet mask
    #default_gateway = "192.168.1.1"  # Replace with the desired default gateway
    dns_servers = "8.8.8.8"  # Replace with the desired DNS servers

    # Get the interface name
    active_interface = psutil.net_if_stats().keys()
    interface_name = next(iter(active_interface), "Local Area Connection")

    # Get user input for DNS servers
    default_gateway = simpledialog.askstring("Default Gateway", "Enter Your Default Gateway:")

    if default_gateway is None:
        return  # User canceled the input

    default_gateway = f'"{default_gateway}"'

    # Confirmation message box
    confirm_message = f"You are about to set the following settings for '{interface_name}':\n\n" \
                      f"Primary IP Address: {primary_ip_address}\n" \
                      f"Secondary IP Address: {secondary_ip_address}\n" \
                      f"Subnet Mask: {subnet_mask}\n" \
                      f"Default Gateway: {default_gateway}\n" \
                      f"DNS Servers: {', '.join(dns_servers)}\n\n" \
                      f"Do you want to continue?"

    if messagebox.askyesno("Confirm Changes", confirm_message):
        set_network_ip(primary_ip_address, subnet_mask, default_gateway, interface_name)
        add_secondary_ip(secondary_ip_address, subnet_mask, interface_name)
        set_dns_settings(dns_servers, interface_name)
        messagebox.showinfo("Set POS3 IP and DNS", "POS3 IP addresses and DNS settings set successfully.")
    else:
        messagebox.showinfo("Set POS3 IP and DNS", "Operation canceled.")
        
def set_pos4_ip_and_dns():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    primary_ip_address = "192.168.9.14"   # Replace with the desired primary IP address for POS4
    secondary_ip_address = "192.168.1.114"  # Replace with the desired secondary IP address for POS4
    subnet_mask = "255.255.255.0"  # Replace with the desired subnet mask
    #default_gateway = "192.168.1.1"  # Replace with the desired default gateway
    dns_servers = "8.8.8.8"  # Replace with the desired DNS servers

    # Get the interface name
    active_interface = psutil.net_if_stats().keys()
    interface_name = next(iter(active_interface), "Local Area Connection")

    # Get user input for DNS servers
    default_gateway = simpledialog.askstring("Default Gateway", "Enter Your Default Gateway:")

    if default_gateway is None:
        return  # User canceled the input

    default_gateway = f'"{default_gateway}"'

    # Confirmation message box
    confirm_message = f"You are about to set the following settings for '{interface_name}':\n\n" \
                      f"Primary IP Address: {primary_ip_address}\n" \
                      f"Secondary IP Address: {secondary_ip_address}\n" \
                      f"Subnet Mask: {subnet_mask}\n" \
                      f"Default Gateway: {default_gateway}\n" \
                      f"DNS Servers: {', '.join(dns_servers)}\n\n" \
                      f"Do you want to continue?"

    if messagebox.askyesno("Confirm Changes", confirm_message):
        set_network_ip(primary_ip_address, subnet_mask, default_gateway, interface_name)
        add_secondary_ip(secondary_ip_address, subnet_mask, interface_name)
        set_dns_settings(dns_servers, interface_name)
        messagebox.showinfo("Set POS4 IP and DNS", "POS4 IP addresses and DNS settings set successfully.")
    else:
        messagebox.showinfo("Set POS4 IP and DNS", "Operation canceled.")

def set_mfs1_ip_and_dns():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    primary_ip_address = "192.168.9.1"   # Replace with the desired primary IP address for MFS1
    secondary_ip_address = "192.168.1.100"  # Replace with the desired secondary IP address for MFS1
    subnet_mask = "255.255.255.0"  # Replace with the desired subnet mask
    #default_gateway = "192.168.1.1"  # Replace with the desired default gateway
    dns_servers = "8.8.8.8"  # Replace with the desired DNS servers

    # Get the interface name
    active_interface = psutil.net_if_stats().keys()
    interface_name = next(iter(active_interface), "Local Area Connection")

    # Get user input for DNS servers
    default_gateway = simpledialog.askstring("Default Gateway", "Enter Your Default Gateway:")

    if default_gateway is None:
        return  # User canceled the input

    default_gateway = f'"{default_gateway}"'

    # Confirmation message box
    confirm_message = f"You are about to set the following settings for '{interface_name}':\n\n" \
                      f"Primary IP Address: {primary_ip_address}\n" \
                      f"Secondary IP Address: {secondary_ip_address}\n" \
                      f"Subnet Mask: {subnet_mask}\n" \
                      f"Default Gateway: {default_gateway}\n" \
                      f"DNS Servers: {', '.join(dns_servers)}\n\n" \
                      f"Do you want to continue?"

    if messagebox.askyesno("Confirm Changes", confirm_message):
        set_network_ip(primary_ip_address, subnet_mask, default_gateway, interface_name)
        add_secondary_ip(secondary_ip_address, subnet_mask, interface_name)
        set_dns_settings(dns_servers, interface_name)
        messagebox.showinfo("Set MFS1 IP and DNS", "MFS1 IP addresses and DNS settings set successfully.")
    else:
        messagebox.showinfo("Set MFS1 IP and DNS", "Operation canceled.")

#------------------------------------------------------------------------------------------------------------

def show_special_feature2():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    url = "https://thecatapi.com/api/images/get?format=src&type=gif"
    webbrowser.open(url)


def chat():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    url = "http://172.232.21.168:3000"
    webbrowser.open(url)


def show_special_feature3():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    url = "https://docs.google.com/document/d/1tY2UITjnd_UXTOJQm0QdVWvbD-ycgeJfG-OUL_6HkvE/edit?usp=sharing"
    webbrowser.open(url)

class ConsoleCapture:
    def __init__(self):
        self.contents = []
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

    def write(self, text):
        self.contents.append(text)
        self.original_stdout.write(text)

    def write_error(self, text):
        self.contents.append(text)
        self.original_stderr.write(text)

    def get_contents(self):
        return ''.join(self.contents)

    def flush(self):
        pass  # Implement this if needed. Many stdlib functions expect this method to exist for stdout/stderr.

console_capture = ConsoleCapture()
sys.stdout = console_capture
sys.stderr = console_capture.write_error

# Function to save logs
def save_logs():
    with open(log_file_path, 'a') as file:
        file.write("Logs saved at " + str(datetime.datetime.now()) + "\n")  # Example log entry
        file.write(console_capture.get_contents() + "\n")
    messagebox.showinfo("Info", "Logs saved successfully!")

# Create the main window
root = tk.Tk()
root.title("Buttonz 3.0.6 - Made by Zee")
root.geometry("640x280")
root.iconbitmap('c:\\buttonz\\icon.ico')

def toggle_edit_mode():
    if edit_mode.get():
        root.configure(bg='white')
        edit_label.pack_forget()
        edit_mode.set(False)
    else:
        root.configure(bg='black')
        edit_label.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=5)
        edit_mode.set(True)
        


# Load the background image using PIL (without resizing)
background_image = Image.open("C:\\Buttonz\\RDS-Logo-NP2.png")

# Convert the PIL image to a PhotoImage
background_photo = ImageTk.PhotoImage(background_image)

# Create a Label widget to display the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window

# Function to resize the background image when the window is resized
def resize_background_image(event):
    global background_image, background_label
    
    # Open the background image
    background_image = Image.open('C:\Buttonz\RDS-Logo-NP2.png')
    
    # Resize the image using the LANCZOS resampling method
    resized_image = background_image.resize((event.width, event.height), Image.LANCZOS)
    
    # Convert the resized image to a PhotoImage and set it as the background label's image
    background_image = ImageTk.PhotoImage(resized_image)
    background_label.config(image=background_image)

# Bind the window resize event
root.bind("<Configure>", resize_background_image)

# Function to generate a random color
def generate_random_color():
    color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return color




# Global dictionary to store the current positions of all buttons
button_positions = {}

class DraggableButton(tk.Button):
    _unique_id = 0  # Class variable to generate unique IDs
    
    def __init__(self, parent, btn_id=None, config_file="button_positions.json", **kwargs):
        super().__init__(parent, **kwargs)
        
        # Generate unique ID if not provided
        if btn_id is None:
            btn_id = f"button{DraggableButton._unique_id}"
            DraggableButton._unique_id += 1
        
        self.btn_id = btn_id
        self.config_file = config_file
        
        # Load initial position from the configuration file
        self.load_position()

        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        
        self.x_offset = 0
        self.y_offset = 0
        self.is_dragging = False  # Flag to check if button is being dragged

        # Unbind the default <ButtonRelease-1> event to prevent automatic command invocation
        self.unbind("<ButtonRelease-1>")

    def on_press(self, event):
        self.x_offset = event.x
        self.y_offset = event.y
        self.is_dragging = False  # Reset dragging flag

    def on_drag(self, event):
        x = event.x_root - self.x_offset - self.master.winfo_rootx()
        y = event.y_root - self.y_offset - self.master.winfo_rooty()
        self.place(x=x, y=y)
        self.is_dragging = True  # Set dragging flag when dragging is detected

    def on_release(self, event):
        
        # Update the global dictionary with the button's position
        global button_positions
        button_positions[self.btn_id] = (self.winfo_x(), self.winfo_y())

        # If the button was not dragged, treat it as a click
        if not self.is_dragging:
            self.invoke()  # Call the button's command

        # Save the button's position when it's released
        self.save_position()
        
        # Reset dragging flag
        self.is_dragging = False

    def save_position(self):
        try:
            print(f"Saving position for {self.btn_id}")
            # Load existing data or initialize an empty dictionary
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    data = json.load(f)
            else:
                data = {}

            # Update the button's position
            data[self.btn_id] = (self.winfo_x(), self.winfo_y())

            # Save the updated data
            with open(self.config_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving position: {e}")
            
    def load_position(self):
        # If config file exists, load the button's position
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                data = json.load(f)
                x, y = data.get(self.btn_id, (50, 50))  # Default position (50, 50)
                self.place(x=x, y=y)
        else:
            self.place(x=50, y=50)  # Default position

# Function to change button colors
def change_button_colors():
    if edit_mode.get():
        print("Edit Mode Active. Command not executed.")
        return
    for button in all_buttons:
        button.config(bg=generate_random_color())

# Function to save the positions of all buttons
def save_all_button_positions():
    for btn in [all_buttons]:  # Add all button instances here
        btn.save_position()


# Create buttons
button1 = DraggableButton(root, text="Open C: Root", command=open_c_drive)

button3 = DraggableButton(root, text="Open Appdata", command=open_appdata_folder)

button7 = DraggableButton(root, text="My Documents", command=lambda: os.startfile(documents_path))

button4 = DraggableButton(root, text="Grab System Specs", command=grab_system_specs)

button5 = DraggableButton(root, text="V8 to Encor", command=run_custom_bat)

button6 = DraggableButton(root, text="Update Balancing", command=edit_and_run_batch)

search_button = DraggableButton(root, text="Searchz", command=run_searchz)

button9 = DraggableButton(root, text="MX9Reboot", command=run_mx9_reboot)

button10 = DraggableButton(root, text="Pinpadinfo", command=run_pinpad_info)

button11 = DraggableButton(root, text="Reload Pinpad", command=edit_and_run_mx9_upgrade)

button2 = DraggableButton(root, text="Install REemv", command=run_custom_exe)

POSDOS_button = DraggableButton(root, text="POSDOS CMD", command=run_posdos)

Epson = DraggableButton(root, text="EpsonOPOS", command=run_custom_exe5)

clear_read_only = DraggableButton(root, text="Clear Read Only(OpenEPS)", command=run_custom_exe4)

dual_test = DraggableButton(root, text="Dual test", command=run_dualtest)

play_pause_button = DraggableButton(root, text="Play Music", command=toggle_music)

change_music_button = DraggableButton(root, text="Change Song", command=change_background_music)

mute_button = DraggableButton(root, text="Volume", command=toggle_mute)

night_mode_button = DraggableButton(root, text="Night Mode", command=toggle_night_mode)

extenz_button = DraggableButton(root, text="Rolodex", command=extenz)

# Collect all buttons in a list for color change
all_buttons = [button1, button2, button3, button4, button5, button6, button7, button9, button10, button11, mute_button, change_music_button, play_pause_button, dual_test, clear_read_only, Epson, search_button, night_mode_button, POSDOS_button, extenz_button]

# Function to save the positions of all buttons
def save_all_button_positions():
    for btn in [button1, button2, button3, button4, button5, button6, button7, button9, button10, button11, mute_button, change_music_button, play_pause_button, dual_test, clear_read_only, Epson, search_button, night_mode_button, POSDOS_button, extenz_button]:  # Add all button instances here
        btn.save_position()

config_path = "C:\\Buttons\\button_positions.json"

# Create a top-level menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create the "File" menu and add it to the menu bar
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save Logs", command=save_logs)
file_menu.add_command(label="Exit", command=root.quit)

# Create the "Tools" menu and add it to the menu bar
tools_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Tools", menu=tools_menu)
tools_menu.add_command(label="ChatGPT", command=run_custom_exe_3)
tools_menu.add_command(label="Edit Mode", command=toggle_edit_mode)
tools_menu.add_command(label="Save Button Layout", command=save_all_button_positions)

edit_label = tk.Label(root, text="Edit Mode", bg='black', fg='red')

# Create the "Options" menu and add it to the menu bar
options_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=options_menu)
options_menu.add_command(label="Check for Update", command=update)
options_menu.add_command(label="Colors!", command=change_button_colors)
options_menu.add_command(label="Help!", command=show_special_feature3)
options_menu.add_command(label="Chat", command=chat)

#---------------------------------------------------------------------------------------------------

# Function to show the context menu for special features
def show_context_menu(event):
    if keyboard.is_pressed('ctrl'):  # Check if Ctrl is held down
        context_menu.post(event.x_root, event.y_root)
        
def show_context_menu(event):
    if keyboard.is_pressed('shift'):  # Check if Shift is held down
        context_menu.post(event.x_root, event.y_root)

root.bind("<Button-3>", show_context_menu)

#------------------------------------------------------------------------------------------------

# Initialize edit mode state 
edit_mode = tk.BooleanVar()
edit_mode.set(False)

# Create the context menu for special features
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Set IP as POS1", command=set_pos1_ip_and_dns)
context_menu.add_command(label="Set IP as POS2", command=set_pos2_ip_and_dns)
context_menu.add_command(label="Set IP as POS3", command=set_pos3_ip_and_dns)
context_menu.add_command(label="Set IP as POS4", command=set_pos4_ip_and_dns)
context_menu.add_command(label="Set IP as MFS1", command=set_mfs1_ip_and_dns)
#context_menu.add_separator()
context_menu.add_separator()
context_menu.add_command(label="Cats!", command=show_special_feature2)
context_menu.add_command(label="Danger Noodle!", command=run_custom_exe_2)

# Run the main loop
root.mainloop()

# Stop the background music when the application is closed
pygame.mixer.music.stop()
pygame.quit()