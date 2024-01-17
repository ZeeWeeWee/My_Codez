import requests
from bs4 import BeautifulSoup
import re
import json

def fetch_and_parse(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            event_list = soup.find(class_='event_list')
            
            # Extract hrefs from all <li> tags
            hrefs = [li.find('a')['href'] for li in event_list.find_all('li') if li.find('a')]

            # Extract and compare groupContentNo
            highest_no = 0
            highest_no_data = None
            for href in hrefs:
                match = re.search(r'groupContentNo=(\d+)', href)
                if match:
                    content_no = int(match.group(1))
                    if content_no > highest_no:
                        highest_no = content_no
                        highest_no_data = href

            return highest_no_data
        else:
            return f"Failed to fetch data. Status code: {response.status_code}"

    except requests.RequestException as e:
        return f"Error during requests: {str(e)}"

def store_data(data, filename='data.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

#def store_data(data, filename='data.json'):
#    with open(filename, 'w') as file:
#        json.dump(data, file, indent=4)

def main():
    print("Starting script...")

    # Informing the user about the fetching process
    print("Fetching data from the website...")
    url = 'https://www.naeu.playblackdesert.com/News/Notice/'
    data = fetch_and_parse(url)

    # Providing feedback based on the data fetched
    if isinstance(data, str) and "groupContentNo" in data:
        print("Highest number data found:", data)

        # Informing the user about the data storage process
        print("Storing data...")
        result = store_data(data)
        print(result)  # Feedback on data storage
    else:
        print("No valid data found or an error occurred:", data)

# Waiting for user input before exiting
input("Press Enter to exit...")

if __name__ == "__main__":
    main()