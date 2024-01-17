import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os

# Create a list to track the player's choices
player_choices = []

# Create a function to change the story text, options, and display images
def change_story(option):
    player_choices.append(option)
    
    if option == 1:
        story_text.config(text="You chose option 1. This is the part of the story where you learn about /insert crisis here\.")
        change_image("Screenshot_1.png")
        button1.config(text="Continue")
        button1.config(command=lambda: change_story(2))
        button2.config(text="New Option")
        button2.config(command=lambda: change_story(3))
        back_button.config(state=tk.NORMAL)  # Enable the back button
    elif option == 2:
        story_text.config(text="You chose option 2. The story continues with learning about such and such issue here")
        change_image("Screenshot_2.png")
        button1.config(text="Option 1")
        button1.config(command=lambda: change_story(4))
        button2.config(text="Option 2")
        button2.config(command=lambda: change_story(5))
    elif option == 3:
        story_text.config(text="You chose A new option. The story continues with learning about such and such issue here")
        change_image("Screenshot_3.png")
        button1.config(text="Option 1")
        button1.config(command=lambda: change_story(6))
        button2.config(text="Option 2")
        button2.config(command=lambda: change_story(7))
    elif option == 4:
        story_text.config(text="You chose A new option. The story continues with learning about such and such issue here")
        change_image("Screenshot_4.png")
        button1.config(text="Option 1")
        button1.config(command=lambda: change_story(8))
        button2.config(text="Option 2")
        button2.config(command=lambda: change_story(9))
    elif option == 5:
        story_text.config(text="You chose A new option. The story continues with learning about such and such issue here")
        change_image("Screenshot_5.png")
        button1.config(text="Option 1")
        button1.config(command=lambda: change_story(10))
        button2.config(text="Option 2")
        button2.config(command=lambda: change_story(11))
    elif option == 6:
        story_text.config(text="You chose A new option. The story continues with learning about such and such issue here")
        change_image("Screenshot_6.png")
        button1.config(text="Option 1")
        button1.config(command=lambda: change_story(12))
        button2.config(text="Option 2")
        button2.config(command=lambda: change_story(13))
    # Add more options, story progression, and image changes as needed

# Create a function to go back to a specific part of the story
def go_back():
    if len(player_choices) > 1:
        # Remove the current choice and go back to the previous choice
        player_choices.pop()
        previous_choice = player_choices[-1]
        change_story(previous_choice)

# Create a function to change the displayed image from the "images" folder
def change_image(image_name):
    image_path = os.path.join("images", image_name)
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.photo = photo

# Create the main window
window = tk.Tk()
window.title("Choose Your Own Crisis")

# Create a label for the story text
story_text = tk.Label(window, text="Welcome to the Artemia crisis training Tool!")
story_text.pack()

# Create an image label
image_label = tk.Label(window)
image_label.pack()

# Create buttons for options
button1 = tk.Button(window, text="Start", command=lambda: change_story(1))
button1.pack()
button2 = tk.Button(window, text="Quit", command=exit)
button2.pack()

# Create a back button (initially disabled)
back_button = tk.Button(window, text="Go Back", command=go_back, state=tk.DISABLED)
back_button.pack()

# Start the game
window.mainloop()
