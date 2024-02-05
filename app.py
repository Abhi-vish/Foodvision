from flask import Flask, render_template,request, session, redirect, url_for,jsonify
from engine import prediction
import os
import classes
from Food import FoodInformation, view_recipe
import json
import requests

app = Flask(__name__, static_url_path="/static")
app.secret_key = "56c1a0d60f933e5fc516b250edaaa98bf6635feb66770a0eda2da3539cadfda5"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect',methods=['GET','POST'])
def detect():
    pred=None
    data=None
    pred_class=None
    if request.method == 'POST':
        image = request.files['image']
        
        if image:
            filename = image.filename
            file_path = os.path.join('static/uploads', filename)
            
            image.save(file_path)
            image_url = '/'+file_path

            try:
                pred =prediction(file_path)
                pred_class = classes.food_items[pred]
                class_name = classes.food_dict.get(pred_class)

                session['food_name'] = class_name

            except Exception as e:
                print('Error: ', str(e))
                print('Invalid image or an error occured during prediction.')
    
            data = {
                "pred":pred,
                "image":file_path,
                "pred_class":class_name,
                }
    return render_template('detect.html',data=data)

@app.route('/foodInformation')
def foodInformation():
    if 'food_name' in session:
        food_name = session['food_name']
        recipe = FoodInformation(food_name)
        # print(recipe)

        return render_template('recipe.html',recipes=recipe,food_name=food_name)
    else:
        return redirect(url_for('index'))

@app.route('/recipe_detail/<int:recipe_id>')
def recipe_detail(recipe_id):
    # Retrieve the recipe details based on the recipe_id
    recipe = view_recipe(recipe_id)  # You'll need to implement this function
    print(recipe)
    if recipe:
        return render_template('view_recipe.html', recipe=recipe)
    return "Recipe not found", 404



@app.route('/MealForIngredients', methods=['GET','POST'])
def MealForIngredient():
    meals=None
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
    return render_template('get_food_by_ingrident.html',meals=meals)


@app.route('/meal_details/<int:meal_id>')
def meal_details(meal_id):
    api_url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}'

    try:
        response = requests.get(api_url)
        data = response.json()
        meal_details = data.get('meals', [])
        return render_template('meal_details.html', meal=meal_details[0])

    
    except Exception as e:
        return jsonify({'error': str(e)})
    
    return render_template('meal_details.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
