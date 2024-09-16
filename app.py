from flask import Flask, render_template, request, jsonify
import requests
from creds import FOOD_API_KEY

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')  # Assumes you have an HTML file named 'index.html'

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
