from req import res
import google.generativeai as genai
from creds import API_KEY

# Configure Google Generative AI with API Key
genai.configure(api_key=API_KEY)

def generate_diet_plan():
    # Prepare the calorie prompt based on calorie results
    output = ""
    for result in res:
        output += f"{result['label']}: {result['calories']} Calories/day ({result['percentage']}) and "

    cal_prompt = output[:-5]

    # Generate content using Google Generative AI
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"write a sample diet plan to meet following requirements {cal_prompt} don't write unnecessary caution and warnings, just write the sample diet plan only")
    
    # Return the generated response text
    return response.text
