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
            
            # Adjusting the search for nested <li> under <ul>
            thumb_nail_list = soup.find(class_='thumb_nail_list')  
        

            # Extract hrefs from all nested <li> tags
            hrefs = [li.find('a')['href'] for li in thumb_nail_list.find_all('li') if li.find('a')]

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

            return highest_no_data or "No matching groupContentNo found."
        else:
            return f"Failed to fetch data. Status code: {response.status_code}"

    except requests.RequestException as e:
        return f"Error during requests: {str(e)}"

def store_data(link, filename='data.json'):
    data = {"link": link}
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

if __name__ == "__main__":
    main()
    
def send_to_discord(webhook_url, message):
    # Payload to be sent to Discord
    data = {"content": message}
    response = requests.post(webhook_url, json=data)

    # Check if the request was successful
    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

def main2():
    json_file = 'data.json'
    webhook_url = 'https://discord.com/api/webhooks/1196661533229453342/7ndq9S_tvhsle8rBXhI2mHQN9w5MSja2OsvCcrgBzQ2Zu906ciuBd4yq2Fzy6pmxkxDF'

    try:
        # Read the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Extract the link (assuming it's under a key named 'link')
        link = data.get('link')

        # Check if the link exists
        if link:
            message = f"Here's your late BDO notice - {link}"
            send_to_discord(webhook_url, message)
        else:
            print("No link found in the JSON file.")

    except Exception as e:
        print(f"An error occurred: {e}")

with open('has run.txt', 'w') as test_file:
    test_file.write('Script has run.')

if __name__ == "__main__":
    main2()
# Waiting for user input before exiting
#input("Press Enter to exit...")
