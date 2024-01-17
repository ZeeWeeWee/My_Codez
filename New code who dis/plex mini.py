import requests

PLEX_URL = 'http://192.168.1.54:32400'
PLEX_TOKEN = '-DceoYFgLSL9ufuKvtk8'

response = requests.get(PLEX_URL, headers={'X-Plex-Token': PLEX_TOKEN})

status_code = response.status_code
response_text = response.text

with open('plex_response.txt', 'w') as f:
    f.write(f"Status Code: {status_code}\n\n")
    f.write("Response Text:\n")
    f.write(response_text)

print(f"Response saved to 'plex_response.txt'")

input("Press Enter to exit...")
