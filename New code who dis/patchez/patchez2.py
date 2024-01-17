import requests
from bs4 import BeautifulSoup
import json

def fetch_and_parse(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Assuming updates are in elements with class 'specific_class_name'
            data = [element.text.strip() for element in soup.find_all(class_='view_detail_area')]
            return data
        else:
            return f"Failed to fetch data. Status code: {response.status_code}"

    except requests.RequestException as e:
        return f"Error during requests: {str(e)}"


def store_data(data, filename='data.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    url = 'https://www.naeu.playblackdesert.com/en-US/News/Detail?groupContentNo=6453&countryType=en-US'
    data = fetch_and_parse(url)
    if isinstance(data, str):
        print(data)
    else:
        store_data(data)
        print("Data successfully fetched and stored.")

with open('has run.txt', 'w') as test_file:
    test_file.write('Script has run.')

if __name__ == "__main__":
    main()

input("Press Enter to exit...")