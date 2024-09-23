from flask import Flask, render_template, request, jsonify
import requests
from creds import FOOD_API_KEY, API_KEY
from req import get_calorie_results
from gen import generate_diet_plan
import markdown

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title = 'Home')

@app.route('/diet')
def diet():
    return render_template('diet.html', title = "Diet")

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get form data
        age = request.form.get('age')
        sex = request.form.get('sex')
        height_feet = request.form.get('height_feet')
        height_inch = request.form.get('height_inch')
        weight_pounds = request.form.get('weight_pounds')
        activity_level = request.form.get('activity_level')
        body_fat_percentage = request.form.get('body_fat_percentage')

        # Fetch calorie results
        res = get_calorie_results(age, sex, height_feet, height_inch, weight_pounds, activity_level, body_fat_percentage)

        # Generate the diet plan using the Generative AI model
        diet_plan_markdown = generate_diet_plan()

        # Convert the diet plan Markdown to HTML
        diet_plan_html = markdown.markdown(diet_plan_markdown)

        # Return the result as JSON including the diet plan in HTML
        return jsonify({
            'calories_result': res,
            'diet_plan_html': diet_plan_html
        })

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/food')
def home():
    return render_template('food.html', title = 'Food')  # Assumes you have an HTML file named 'index.html'

@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    recipe_name = request.form.get('recipeName')
    selected_cuisine = request.form.get('cuisine')
    
    try:
        # Step 1: Search for the recipe by name (with optional cuisine filter)
        search_url = f'https://api.spoonacular.com/recipes/complexSearch?query={recipe_name}&apiKey={FOOD_API_KEY}'
        
        # If a specific cuisine is selected, add the cuisine parameter to the URL
        if selected_cuisine:
            search_url += f'&cuisine={selected_cuisine}'

        search_response = requests.get(search_url)
        search_data = search_response.json()

        if len(search_data['results']) == 0:
            return jsonify({'error': f'No recipe found for "{recipe_name}".'})
        
        # Get the first recipe's ID and image URL
        recipe = search_data['results'][0]
        recipe_id = recipe['id']
        recipe_image = recipe['image']

        # Step 2: Get the nutritional information for the recipe
        nutrition_url = f'https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json?apiKey={FOOD_API_KEY}'
        nutrition_response = requests.get(nutrition_url)
        nutrition_data = nutrition_response.json()

        # Return recipe details
        return jsonify({
            'recipeName': recipe_name,
            'calories': nutrition_data['calories'],
            'fat': nutrition_data['fat'],
            'carbs': nutrition_data['carbs'],
            'protein': nutrition_data['protein'],
            'image': recipe_image
        })

    except Exception as e:
        print('Error fetching data:', e)
        return jsonify({'error': 'Error fetching data. Please try again.'})

if __name__ == '__main__':
    app.run(debug=True)
