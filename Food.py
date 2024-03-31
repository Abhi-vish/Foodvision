import requests
from urllib.parse import unquote
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.environ.get("spoonacular_api")

# For getting recipe details
def search_recipe(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey':api_key,
        'query':query,
        'number':10,
        'instructionsRequired':True,
        'addRecipeInformation':True,
        'fillIngredients':True
    }

    # Sending GET request to api
    response = requests.get(url, params=params)
    print(response)
    # if the API call is successful
    if response.status_code == 200:
        # Parse the API response as JSON Data
        data = response.json()
        # Return the list of recipe
        return data['results']

    # If not successful 
    return []

def FoodInformation(class_name):

    recipe = search_recipe(class_name)
    return recipe


# For getting the information of a specific food
def view_recipe(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': api_key,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipe = response.json()
        return recipe
    return 'Recipe not found',404


# Getting nutritional information
def get_food_nutrition(product_id):
    url = f'https://api.spoonacular.com/food/products/{product_id}'
    params = {
        'apiKey': api_key
    }

    # Sending GET request to api
    response = requests.get(url, params=params)

    # if the API call is successful
    if response.status_code == 200:
        # Parse the API response as JSON Data
        data = response.json()
        # Return the detailed nutritional information for the product
        nutrition_info = data.get('nutrition', {})
        return nutrition_info

    # If not successful
    return {}

def search_food_nutrition(query):
    url = f'https://api.spoonacular.com/food/products/search'
    params = {
        'apiKey': api_key,
        'query': query,
        'number': 1
    }

    # Sending GET request to api
    response = requests.get(url, params=params)

    # if the API call is successful
    if response.status_code == 200:
        # Parse the API response as JSON Data
        data = response.json()
        
        # Check if products are found
        if data['totalProducts'] > 0:
            product_id = data['products'][0]['id']
            nutrition_info = get_food_nutrition(product_id)
            return nutrition_info

    # If not successful
    return {}


# Function to get restaurant search response

# Function to get restaurant search response
def get_restaurant_search(query):
    url = 'https://api.spoonacular.com/food/restaurants/search'
    params = {
        'apiKey': api_key,
        'query': query,
        'lat': 19.2183,
        'lng': 72.9781,
        'distance': 5
    }

    # Sending GET request to the API
    response = requests.get(url, params=params)

    # Check if the API call is successful
    if response.status_code == 200:
        # Parse the API response as JSON data
        data = response.json()
        # Return the response data
        return data

    # If not successful
    return None


# Nutritional Label
def get_nutrition_label_image(recipe_id, filename=None):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/nutritionLabel.png'
    params = {'apiKey': api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        if filename is None:
            filename = f'static/neutritional_img/Neutritional.png'  # Changed filename to include folder path
        else:
            filename = f'static/neutritional_img/{filename}'  
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        return f"Error: {response.status_code} - {response.text}"
