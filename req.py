import requests
from bs4 import BeautifulSoup

# Function to fetch and display calorie results based on input parameters
def get_calorie_results(age, sex, height_feet, height_inch, weight_pounds, activity_level, body_fat_percentage):
    # Create a dictionary for the parameters
    params = {
        "cage": age,
        "csex": sex,
        "cheightfeet": height_feet,
        "cheightinch": height_inch,
        "cpound": weight_pounds,
        "cactivity": activity_level,
        "cfatpct": body_fat_percentage,
        "coutunit": "c",  # Output unit (Calories, KiloJoules)
        "cformula": "m",  # Formula for calculation (Mifflin-St Jeor, Revised Harris-Benedict, Katch-McArdle)
        "cmop": 1,        # For metric output
        "ctype": "standard", # Output type (standard)
        "printit": 0,      # No need to print
        "x": "Calculate"   # Action (calculate)
    }

    # Send the GET request
    response = requests.get("https://www.calculator.net/calorie-calculator.html", params=params)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract and print the results from the table
    table = soup.find('table')
    if not table:
        print("No results found.")
        return

    results = []
    for row in table.find_all('tr'):
        data = {}

        # Extract the label (Maintain weight, Mild weight loss, etc.)
        data['label'] = row.find('div', class_='bigtext').text.strip()

        # Check if there's a subtitle (e.g., 0.5 lb/week)
        subtitle = row.find('div', style='color:#888;')
        if subtitle:
            data['subtitle'] = subtitle.text.strip()

        # Extract the calorie value and percentage
        result_box = row.find('div', class_='verybigtext')
        data['calories'] = result_box.find('b').text.strip()
        data['percentage'] = result_box.find('span', class_='smalltext').text.strip()

        results.append(data)

    # Print the results in a readable format
    return results

# Example usage: Change parameters as needed
age = 70 #ranges from 15-80 years
sex = "f"
height_feet = 5
height_inch = 6
weight_pounds = 200
activity_level = 1.55  # Moderate activity
#sedentary = 1.2 , light = 1.375, moderate = 1.465, active = 1.65, very active = 1.725, extra active = 1.9
body_fat_percentage = 20 #percentage

# Fetch and print the results
res = get_calorie_results(age, sex, height_feet, height_inch, weight_pounds, activity_level, body_fat_percentage)