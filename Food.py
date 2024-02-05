import requests
from urllib.parse import unquote
import os
from dotenv import load_dotenv
import json

api_key = "f9910a7dadd8495a9cec5d6bd8418c8c"

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
    print(api_key)
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
