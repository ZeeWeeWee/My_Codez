import json
import requests

def send_to_discord(webhook_url, message):
    # Payload to be sent to Discord
    data = {"content": message}
    response = requests.post(webhook_url, json=data)

    # Check if the request was successful
    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

def main():
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
    main()

input("Press Enter to exit...")