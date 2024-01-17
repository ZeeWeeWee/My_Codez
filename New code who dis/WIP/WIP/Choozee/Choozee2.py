import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os

# Create a list to track the player's choices
player_choices = []

# Create a dictionary to map choice numbers to functions
choice_functions = {
    1: lambda: choice_1(),
    2: lambda: choice_2(),
    3: lambda: choice_3(),
    4: lambda: choice_4(),
    5: lambda: choice_5(),
    6: lambda: choice_6(),
    # Add more choices as needed
}

# Define your choice functions
def choice_1():
    story_text.config(text="Your boss get a call and the stocks are down! This is a disaster! What happened?.")
    change_image("Screenshot_1.png")
    button1.config(text="Go to Starbucks")
    button1.config(command=lambda: change_story(2))
    button2.config(text="Listen in")
    button2.config(command=lambda: change_story(3))

def choice_2():
    story_text.config(text="Your CFO Left his laptop out in starbucks whilst he went and took a leak and it got hacked")
    change_image("Screenshot_2.png")
    button1.config(text="Console Him")
    button1.config(command=lambda: change_story(4))
    button2.config(text="Fire him")
    button2.config(command=lambda: change_story(5))

def choice_3():
    story_text.config(text="Your Employees are on strike as they are tired of all the robots taking there jobs!")
    change_image("Screenshot_3.png")
    button1.config(text="Speak with them")
    button1.config(command=lambda: change_story(6))
    button2.config(text="Murder them! (allegedly)")
    button2.config(command=lambda: change_story(7))

def  choice_4():
    story_text.config(text="You chose to console your CFO Hes a dumbass but it can happen to anyone")
    change_image("Screenshot_5.png")
    button1.config(text="Give him a training course")
    button1.config(command=exit)
    button2.config(text="Hire a tutor")
    button2.config(command=exit)

def  choice_5():
    story_text.config(text="You chose to fire your CFO! How could anyone be so Stupid!")
    change_image("Screenshot_6.png")
    button1.config(text="Make a big show of it")
    button1.config(command=exit)
    button2.config(text="Throw him out the window to get rid of the filth faster")
    button2.config(command=exit)

def  choice_6():
    story_text.config(text="You chose to be a decent Boss and Humand and listen to your employees Grief")
    change_image("Screenshot_4.png")
    button1.config(text="Give them a Raise!")
    button1.config(command=exit)
    button2.config(text="Give them more time off")
    button2.config(command=exit)
    # Add more choice functions as needed

# Create a function to change the story text, options, and display images
def change_story(option):
    if option in choice_functions:
        player_choices.append(option)
        choice_functions[option]()
        back_button.config(state=tk.NORMAL)  # Enable the back button

# Create a function to go back to a specific part of the story
def go_back():
    if len(player_choices) > 1:
        # Remove the current choice and go back to the previous choice
        player_choices.pop()
        previous_choice = player_choices[-1]
        choice_functions[previous_choice]()

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
button2 = tk.Button(window, text="Exit", command=exit)
button2.pack()

# Create a back button (initially disabled)
back_button = tk.Button(window, text="Go Back", command=go_back, state=tk.DISABLED)
back_button.pack()

# Start the game
window.mainloop()
