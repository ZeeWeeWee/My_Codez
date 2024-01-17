import requests

# Replace with your Plex server URL and token
PLEX_URL = 'http://192.168.1.54:32400'
PLEX_TOKEN = '-DceoYFgLSL9ufuKvtk8'

def get_unwatched_media(section_key):
    headers = {'X-Plex-Token': PLEX_TOKEN}
    
    # Retrieve library data for the specified section
    section_url = f'{PLEX_URL}/library/sections/{section_key}/all'

    # Debug print
    print(f"Fetching data for section {section_key} from URL: {section_url}")

    section_response = requests.get(section_url, headers=headers)

    # Debug print
    print(f"Response status code: {section_response.status_code}")

    section_data = section_response.json()

    unwatched_media = []

    for video in section_data['MediaContainer']['Metadata']:
        if not video['viewCount']:
            unwatched_media.append(video['title'])

    return unwatched_media

if __name__ == "__main__":
    unwatched_movies = get_unwatched_media('MOVIES')
    unwatched_tv_shows = get_unwatched_media('TV_SHOWS')
    unwatched_anime = get_unwatched_media('ANIME')
    
    print("Unwatched Movies:")
    for movie in unwatched_movies:
        print(movie)

    print("\nUnwatched TV Shows:")
    for show in unwatched_tv_shows:
        print(show)
        
    print("\nUnwatched Anime:")
    for anime in unwatched_anime:
        print(anime)
