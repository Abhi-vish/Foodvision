from flask import Flask, render_template,request,session, jsonify,session, redirect,url_for
import os
import requests

import classes
from engine import prediction
from Food import search_food_nutrition, view_recipe, FoodInformation, get_restaurant_search,get_nutrition_label_image
from resturant import get_place,get_place_by_place_id

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from chatbot import prompt
from chatbot import api_key


app_secret_key = os.environ.get('app_secret_key')
llm = ChatGoogleGenerativeAI(model='gemini-pro',
                             google_api_key=api_key)

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt
)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)  # Generate a secret key


@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form['user_input']
    output = llm_chain.run(user_input)
    print(f"Input: {user_input}\nOutput: {output}")

    session['input']=user_input
    session['output']=output
    return jsonify({'input': user_input, 'result': output})

@app.route('/')
def home():
    # Assuming input and output are stored in session, modify as needed
    input_data = session.get('input')
    output_data = session.get('output')

    return render_template('home.html',input_data=input_data, output_data=output_data)

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/information', methods=['GET','POST'])
def get_information():
    pred=None
    data=None
    class_name=''
    nutrition_info = None

    if request.method == 'POST':
        image = request.files['image']
        
        if image:
            filename = image.filename
            file_path = os.path.join('static/uploads', filename)
            
            image.save(file_path)
            image_url = '/'+file_path

            try:
                pred = prediction(file_path)
                print(pred)
                class_name = classes.food_dict.get(classes.food_items[pred])
                nutrition_info = search_food_nutrition(class_name)

                session['food_name'] = class_name

            except Exception as e:
                print('Error: ', str(e))
                print('Invalid image or an error occurred during prediction.')

    data = {
        "pred": pred,
        "image": file_path,
        "pred_class": class_name,
        "nutrition": nutrition_info
        }
    return render_template('information.html', data=data)


@app.route("/foodInformation")
def foodInformation():
    try:
        food_name = session.get('food_name')  # Use session.get() to avoid KeyError
        if food_name:
            recipe = FoodInformation(food_name)
            no_recipe = len(recipe)
            print(no_recipe)
            return render_template('card.html', food_name=food_name, recipes=recipe, no_recipe=no_recipe)
        else:
            return render_template('error.html', message='Food name not found in session')
    except Exception as e:
        return render_template('error.html', e=e)


@app.route('/recipe_detail/<int:recipe_id>')
def recipe_detail(recipe_id):
    try:
        # Retrieve the recipe details based on the recipe_id
        recipe = view_recipe(recipe_id)  # You'll need to implement this function
        food_name = session['food_name']
        ingredients = recipe.get('extendedIngredients', [])
        ing_counts = len(ingredients)
        neutritional_img = get_nutrition_label_image(recipe_id=recipe_id)
        data = {
            "img": neutritional_img
        }

        # print(recipe)
        if recipe:
            return render_template('view_recipe.html', recipe=recipe, food_name=food_name, ing_counts=ing_counts, data=data)
        return "Recipe not found", 404
    except KeyError:
        return render_template('error.html', message='Food name not found in session')
    

@app.route("/restaurants")
def restaurants():
    if 'food_name' in session:
        food_name = session['food_name']
        local_result = get_place(food=food_name,location='19.2183,72.9781')
        print(local_result)
         # Check if local_result is None or empty
            
        if local_result is None or not local_result:
            local_results = []  # Set local_results to an empty list
        else:
            # If local_result is not None and not empty, assign it to local_results
            local_results = local_result

        return render_template('resturants.html',food_name=food_name,local_results=local_results)
    else:
        print('Error 404')

@app.route('/location_detail/<place_id>')
def location_detail(place_id):
    # Retrieve the recipe details based on the recipe_id
    place = get_place_by_place_id(place_id=place_id)  # You'll need to implement this function
    food_name = session['food_name']

    # print(recipe)
    if place:
        return render_template('place_details.html', place_detail=place,food_name=food_name)
    return "Recipe not found", 404




@app.route('/MealForIngredients', methods=['GET','POST'])
def MealForIngredient():
    meals=None
    ingredient=None
    if request.method == "POST":
        ingredient = request.form.get('ingredient')

        api_url = f'https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}'

        try:
            response = requests.get(api_url)
            data = response.json()
            meals = data.get('meals', [])

        except Exception as e:
            return jsonify({'error': str(e)})

    # Return a response for other HTTP methods (e.g., GET)
    return render_template('get_food_by_ingrident.html',meals=meals,ingredient=ingredient)


@app.route('/meal_details/<int:meal_id>')
def meal_details(meal_id):
    api_url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}'

    try:
        response = requests.get(api_url)
        data = response.json()
        meal_details = data.get('meals', [])
        print(meal_details)
        return render_template('meal.html', meal=meal_details[0])

    
    except Exception as e:
        return jsonify({'error': str(e)})
    
    return render_template('meal_details.html')




@app.route('/card')
def card():
    return render_template('places.html')





if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
