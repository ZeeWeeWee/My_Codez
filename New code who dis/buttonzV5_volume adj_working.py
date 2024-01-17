import tkinter as tk
from tkinter import messagebox
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



# Initialize pygame
pygame.mixer.init()

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

# Function to grab and display system specs
def grab_system_specs():
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

# Function to open C: drive
def open_c_drive():
    os.startfile("C:")

# Function to run a custom executable
def run_custom_exe():
    exe_path = 'C:\\Buttonz\\REemv_Setup.exe'
    os.startfile(exe_path)

# Function to open AppData folder
def open_appdata_folder():
    os.startfile(appdata_path)

# Function to run the specified bat file
def run_custom_bat():
    bat_path = 'C:\\Buttonz\\V8toE_1.7.bat'
    subprocess.Popen(['cmd.exe', '/C', bat_path], shell=True)

# Function to open and edit a batch file, then run it
def edit_and_run_batch():
    batch_path = 'C:\\Buttonz\\updbal.bat'
    try:
        subprocess.Popen(['notepad.exe', batch_path]).wait()
        subprocess.Popen(['cmd.exe', '/C', batch_path], shell=True)
    except Exception as e:
        print(f"Error editing and running batch file: {e}")

# Function to run MX9Reboot.exe
def run_mx9_reboot():
    exe_path = 'C:\\Buttonz\\MX9Reboot.exe'
    os.startfile(exe_path)

# Function to run Pinpadinfo.exe
def run_pinpad_info():
    exe_path = 'C:\\Buttonz\\Pinpadinfo.exe'
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
    global current_song, song_position  # Add this line to access the global variables
    pygame.mixer.music.stop()
    current_song = choose_random_background()  # Change the current song
    song_position = 0  # Reset the song position
    toggle_music()

# Play the background music
song_path = choose_random_background()
pygame.mixer.music.load(song_path)
pygame.mixer.music.play(-1)  # Loop the song indefinitely





def edit_and_run_mx9_upgrade():
    mx9_ini_path = 'C:\\Buttonz\\MX9UPG\\MX9.ini'
    up_mx_bat_path = 'C:\\Buttonz\\MX9UPG\\UP-MX F1 Run as Admin.bat'

    try:
        # Open MX9.ini in Notepad
        subprocess.Popen(['notepad.exe', mx9_ini_path]).wait()

        # Save the edited MX9.ini file to a temporary location
        mx9_ini_temp_path = 'C:\\Buttonz\\MX9UPG\\MX9_temp.ini'
        shutil.copy(mx9_ini_path, mx9_ini_temp_path)

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


# Create the main window
root = tk.Tk()
root.title("Buttonz 1.2.5")
root.geometry("640x264")



# Load the background image using PIL (without resizing)
background_image = Image.open("C:\\Buttonz\\RDS-Logo-NP2.png")

# Convert the PIL image to a PhotoImage
background_photo = ImageTk.PhotoImage(background_image)

# Create a Label widget to display the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window







# Rest of your button creation code...

# Function to generate a random color
def generate_random_color():
    color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return color

# Function to change button colors
def change_button_colors():
    for button in all_buttons:
        button.config(bg=generate_random_color())



# Create buttons
button1 = tk.Button(root, text="Open C: Root", command=open_c_drive)
button1.grid(row=0, column=0, padx=10, pady=10)

button3 = tk.Button(root, text="Open Appdata", command=open_appdata_folder)
button3.grid(row=0, column=1, padx=10, pady=10)

button2 = tk.Button(root, text="Install REemv", command=run_custom_exe)
button2.grid(row=0, column=2, padx=10, pady=10)

button4 = tk.Button(root, text="Grab System Specs", command=grab_system_specs)
button4.grid(row=0, column=3, padx=10, pady=10)

button5 = tk.Button(root, text="V8 to Encor", command=run_custom_bat)
button5.grid(row=0, column=4, padx=10, pady=10)

button6 = tk.Button(root, text="Update Balancing", command=edit_and_run_batch)
button6.grid(row=1, column=4, padx=10, pady=10)

button7 = tk.Button(root, text="My Documents", command=lambda: os.startfile(documents_path))
button7.grid(row=1, column=0, padx=10, pady=10)

button8 = tk.Button(root, text="Change Button Colors :3", command=change_button_colors)
button8.grid(row=1, column=2, padx=10, pady=10)

button9 = tk.Button(root, text="MX9Reboot", command=run_mx9_reboot)
button9.grid(row=2, column=0, padx=10, pady=10)

button10 = tk.Button(root, text="Pinpadinfo", command=run_pinpad_info)
button10.grid(row=2, column=1, padx=10, pady=10)

# Create a button to edit MX9.ini and run UP-MX F1 Run as Admin.bat
button11 = tk.Button(root, text="Reload Pinpad", command=edit_and_run_mx9_upgrade)
button11.grid(row=2, column=2, padx=10, pady=10)

# Mute button
mute_button = tk.Button(root, text="Volume", command=toggle_mute)
mute_button.grid(row=3, column=4, padx=10, pady=5)

# Create a button to change the background music
change_music_button = tk.Button(root, text="Change Song", command=change_background_music)
change_music_button.grid(row=3, column=2, padx=10, pady=5)

# Create a button to play or pause background music
play_pause_button = tk.Button(root, text="Pause Music", command=toggle_music)
play_pause_button.grid(row=3, column=3, padx=10, pady=5)
# Collect all buttons in a list for color change

all_buttons = [button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11, mute_button, change_music_button]

all_buttons.append(play_pause_button)








# Run the main loop
root.mainloop()

# Stop the background music when the application is closed
pygame.mixer.music.stop()
pygame.quit()