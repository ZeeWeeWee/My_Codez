import requests
import webbrowser

def open_random_cat_gif():
    url = "https://thecatapi.com/api/images/get?format=src&type=gif"
    response = requests.get(url)
    if response.status_code == 200:
        webbrowser.open(response.url)
    else:
        print("Failed to fetch a cat GIF.")

open_random_cat_gif()