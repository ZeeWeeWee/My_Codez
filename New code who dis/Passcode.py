import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

def generate_password():
    try:
        length = int(length_entry.get())
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = string.punctuation
        all = lower + upper + num + symbols
        temp = random.sample(all, length)
        password = "".join(temp)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for password length")

def copy_to_clipboard():
    pyperclip.copy(password_entry.get())
    messagebox.showinfo("Copied", "Password copied to clipboard")

def save_to_file():
    password = password_entry.get()
    with open('password.txt', 'w') as f:
        f.write(password)
    messagebox.showinfo("Saved", "Password saved to password.txt")

# Set up the window
root = tk.Tk()
root.title("Password Generator")

# Length input
length_label = tk.Label(root, text="Enter password length:")
length_label.pack()
length_entry = tk.Entry(root)
length_entry.pack()

# Password display
password_label = tk.Label(root, text="Generated Password:")
password_label.pack()
password_entry = tk.Entry(root, width=40)
password_entry.pack()

# Generate button
generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.pack()

# Copy button
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack()

# Save button
save_button = tk.Button(root, text="Save to File", command=save_to_file)
save_button.pack()

# Start the GUI
root.mainloop()
