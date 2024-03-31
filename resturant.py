import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("alter_2_serpapi_key")

def get_place(food, location='Thane, Mumbai'):
    local_results = None
    serpapi_url = 'https://serpapi.com/search.json'

    params = {
        'engine': 'google_maps',
        'q': food,
        'll': f'@{location},15z',
        'type': 'search',
        'api_key': api_key,
    }

    try:
        response = requests.get(serpapi_url, params=params)
        response.raise_for_status()  # Raise an exception for 4XX or 5XX errors

        data = response.json()
        local_results = data.get('local_results', [])

        for item in local_results:
            photos_link = item.get('photos_link')

            if photos_link:
                photo_response = requests.get(photos_link, params={'api_key': api_key})
                photo_response.raise_for_status()  # Raise an exception for 4XX or 5XX errors

                photo_data = photo_response.json()
                # Do something with photo_data if needed

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return local_results


def get_place_by_place_id(place_id):
    serpapi_url = 'https://serpapi.com/search.json'

    params = {
        'engine': 'google_maps',
        'place_id': place_id,
        'api_key': api_key
    }

    try:
        response = requests.get(serpapi_url, params=params)
        response.raise_for_status()  # Raise an exception for 4XX or 5XX errors

        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
