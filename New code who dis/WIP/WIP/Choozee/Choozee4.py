import tkinter as tk
from tkinter import PhotoImage
from tkinter.ttk import Separator
from PIL import Image, ImageTk
import os

# Create a list to track the player's choices
player_choices = []
player_choices2 = []
storyline = "social_media"

# Create a dictionary to map choice numbers to functions for the "Company Crisis" storyline
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

# Define your choice functions for the "Company Crisis" storyline
def choice_1_company():
    global storyline  # Declare storyline as a global variable
    storyline = "company"  # Update the storyline variable
    story_text.config(text="Your boss gets a call, and the stocks are down! This is a disaster! What happened.")
    change_image("Screenshot_1.png")
    button1.config(text="Go to Starbucks")
    button1.config(command=lambda: change_story(2, "company"))
    button2.config(text="Listen in")
    button2.config(command=lambda: change_story(3, "company"))

def choice_2_company():
    story_text.config(text="Your CFO Left his laptop out in Starbucks while he went for a break, and it got hacked.")
    change_image("Screenshot_2.png")
    button1.config(text="Console Him")
    button1.config(command=lambda: change_story(4, "company"))
    button2.config(text="Fire him")
    button2.config(command=lambda: change_story(5, "compamy"))

def choice_3_company():
    story_text.config(text="Your employees are on strike as they are tired of all the robots taking their jobs!")
    change_image("Screenshot_3.png")
    button1.config(text="Speak with them")
    button1.config(command=lambda: change_story(6, "company"))
    button2.config(text="Murder them! (allegedly)")
    button2.config(command=lambda: change_story(7, "company"))

def  choice_4_company():
    story_text.config(text="You chose to console your CFO. He's a dumbass but it can happen to anyone.")
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
    story_text.config(text="You chose to be a decent Boss and listen to your employees' grief.")
    change_image("Screenshot_4.png")
    button1.config(text="Give them a Raise!")
    button1.config(command=exit)
    button2.config(text="Give them more time off")
    button2.config(command=exit)
    # Add more choice functions as needed

# Define choice functions for the "Social Media Crisis" storyline
def choice_1_social_media():
    global storyline  # Declare storyline as a global variable
    storyline = "social_media"  # Update the storyline variable
    story_text.config(text="A social media scandal erupts as your company is trending for all the wrong reasons. What do you do?")
    change_image("social (1).jpg")
    button1.config(text="Respond with an apology")
    button1.config(command=lambda: change_story(2, "social_media"))
    button2.config(text="Ignore it and hope it blows over")
    button2.config(command=lambda: change_story(3, "social_media"))

def choice_2_social_media():
    story_text.config(text="Your company's confidential customer data has been breached, and it's spreading like wildfire on social media.")
    change_image("social (2).jpg")
    button1.config(text="Notify affected customers and authorities")
    button1.config(command=lambda: change_story(4, "social_media"))
    button2.config(text="Downplay the breach and deny responsibility")
    button2.config(command=lambda: change_story(5, "social_media"))

def choice_3_social_media():
    story_text.config(text="Unfounded rumors about a product defect are causing panic on social media.")
    change_image("social (3).jpg")
    button1.config(text="Investigate the issue and issue a statement if necessary")
    button1.config(command=lambda: change_story(6, "social_media"))
    button2.config(text="Ignore the rumors and hope they fade away")
    button2.config(command=lambda: change_story(7, "social_media"))


def change_story(option, storyline):
    if storyline == "company" and option in choice_functions_company:
        player_choices.append(option)
        choice_functions_company[option]()
    elif storyline == "social_media" and option in choice_functions_social_media:
        player_choices.append(option)
        choice_functions_social_media[option]()

# Create a function to go back to a specific part of the story
def go_back():
    if len(player_choices) > 1:
        # Remove the current choice and go back to the previous choice
        current_choice = player_choices.pop()
        player_choices2.append(current_choice)  # Move the choice to player_choices2
        previous_choice = player_choices[-1]
        if storyline == "company":
            choice_functions_company[previous_choice]()
        elif storyline == "social_media":
            choice_functions_social_media[previous_choice]()


# Create a function to change the displayed image from the "images" folder
def change_image(image_name):
    image_path = os.path.join("images", image_name)
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.photo = photo

# Create a function to go back to the first screen
def go_to_home():
    player_choices.clear()  # Clear the player's choices
    story_text.config(text="Welcome to the Artemia crisis training Tool!")
    change_image("welcome_image.jpg")  # Change this to your welcome image
    button1.config(text="Company Crisis", command=lambda: change_story(1, "company"))
    button2.config(text="Social Media Crisis", command=lambda: change_story(1, "social_media"))

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
separator = Separator(window, orient="horizontal")
separator.pack()
button2 = tk.Button(window, text="Social Media Crisis", command=lambda: change_story(1, "social_media"))
button2.pack()
separator = Separator(window, orient="horizontal")
separator.pack()
back_button = tk.Button(window, text="Go Back", command=go_back)
back_button.pack()
separator = Separator(window, orient="horizontal")
separator.pack()
button3 = tk.Button(window, text="Exit", command=exit)
button3.pack()

# Create a button for going back to the first screen
home_button = tk.Button(window, text="Home", command=go_to_home)
home_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Call go_to_home() to show the home screen when the application is launched
go_to_home()

# Start the game
window.mainloop()
