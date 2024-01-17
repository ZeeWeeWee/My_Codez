import tkinter as tk
import keyboard  # Make sure you have the 'keyboard' module installed

# Function to show the context menu for special features
def show_context_menu(event):
    if keyboard.is_pressed('ctrl'):  # Check if Ctrl is held down
        context_menu.post(event.x_root, event.y_root)

# Create a context menu
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Option 1", command=lambda: print("Option 1 clicked"))
context_menu.add_command(label="Option 2", command=lambda: print("Option 2 clicked"))
context_menu.add_separator()
context_menu.add_command(label="Exit", command=root.quit)

# Bind the right-click event to show the context menu
root.bind("<Button-3>", show_context_menu)

# Run the main loop
root.mainloop()
