import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os

# Create a list to track the player's choices
player_choices = []
player_choices2 = []

# Create a dictionary to map choice numbers to functions
choice_functions_company = {
    1: lambda: choice_1_company(),
    2: lambda: choice_2_company(),
    3: lambda: choice_3_company(),
    4: lambda: choice_4_company(),
    5: lambda: choice_5_company(),
    6: lambda: choice_6_company(),
    # Add more choices as needed for the "Company Crisis" storyline
}

# Create a dictionary to map choice numbers to functions for the "Social Media Crisis" storyline
choice_functions_social_media = {
    1: lambda: choice_1_social_media(),
    2: lambda: choice_2_social_media(),
    3: lambda: choice_3_social_media(),
    4: lambda: choice_4_social_media(),
    5: lambda: choice_5_social_media(),
    6: lambda: choice_6_social_media(),
    # Add more choices as needed for the "Social Media Crisis" storyline
}

# Define your choice functions
def choice_1_company():
    story_text.config(text="Your boss gets a call, and the stocks are down! This is a disaster! What happened?")
    change_image("Screenshot_1.png")
    button1.config(text="Go to Starbucks")
    button1.config(command=lambda: change_story(2, "company"))
    button2.config(text="Listen in")
    button2.config(command=lambda: change_story(3, "company"))

def choice_2_company():
    story_text.config(text="Your CFO Left his laptop out in starbucks whilst he went and took a leak and it got hacked")
    change_image("Screenshot_2.png")
    button1.config(text="Console Him")
    button1.config(command=lambda: change_story(4))
    button2.config(text="Fire him")
    button2.config(command=lambda: change_story(5))

def choice_3_company():
    story_text.config(text="Your Employees are on strike as they are tired of all the robots taking there jobs!")
    change_image("Screenshot_3.png")
    button1.config(text="Speak with them")
    button1.config(command=lambda: change_story(6))
    button2.config(text="Murder them! (allegedly)")
    button2.config(command=lambda: change_story(7))

def  choice_4_company():
    story_text.config(text="You chose to console your CFO Hes a dumbass but it can happen to anyone")
    change_image("Screenshot_5.png")
    button1.config(text="Give him a training course")
    button1.config(command=exit)
    button2.config(text="Hire a tutor")
    button2.config(command=exit)

def  choice_5_company():
    story_text.config(text="You chose to fire your CFO! How could anyone be so Stupid!")
    change_image("Screenshot_6.png")
    button1.config(text="Make a big show of it")
    button1.config(command=exit)
    button2.config(text="Throw him out the window to get rid of the filth faster")
    button2.config(command=exit)

def  choice_6_company():
    story_text.config(text="You chose to be a decent Boss and Humand and listen to your employees Grief")
    change_image("Screenshot_4.png")
    button1.config(text="Give them a Raise!")
    button1.config(command=exit)
    button2.config(text="Give them more time off")
    button2.config(command=exit)
    # Add more choice functions as needed

# Define choice functions for the "Social Media Crisis" storyline
def choice_1_social_media():
    story_text.config(text="A social media scandal erupts as your company is trending for all the wrong reasons. What do you do?")
    change_image("social (1).jpg")
    button1.config(text="Respond with an apology")
    button1.config(command=lambda: change_story(2, "social_media"))
    button2.config(text="Ignore it and hope it blows over")
    button2.config(command=lambda: change_story(3, "social_media"))

# Create a function to change the story text, options, and display images
def change_story(option, storyline="company"):
    if storyline == "company" and option in choice_functions_company:
        player_choices.append(option)
        choice_functions_company[option]()
        toggle_social_media_button("company")
    elif storyline == "social_media" and option in choice_functions_social_media:
        player_choices.append(option)
        choice_functions_social_media[option]()
        toggle_social_media_button("social_media")

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

# Create buttons for options for both storylines
button1 = tk.Button(window, text="Company Crisis", command=lambda: change_story(1, "company"))
button1.pack()
button2 = tk.Button(window, text="Social Media Crisis", command=lambda: change_story(1, "social_media"))
button2.pack()
back_button = tk.Button(window, text="Go Back", command=go_back, state=tk.DISABLED)
back_button.pack()
button3 = tk.Button(window, text="Exit", command=exit)
button3.pack()

# Create a back button (initially disabled)


# Start the game
window.mainloop()


# Start the game
window.mainloop()
