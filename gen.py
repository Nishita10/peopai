from req import res
import google.generativeai as genai
from creds import API_KEY

output = ""
for result in res:
    output += f"{result['label']}: {result['calories']} Calories/day ({result['percentage']}) and "

cal_prompt = output[:-5]

genai.configure(api_key=API_KEY)

place = 'nepal'
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(f"write a sample diet plan to meet following requirements {cal_prompt} don't write unnecessary caution and waring just write the sample diet plan only")
print(response.text)

