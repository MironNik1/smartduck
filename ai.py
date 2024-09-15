import google.generativeai as genai
from configs.aicfg import *

def AIGenerate(prompt):
    genai.configure(api_key=KEY)
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)
    return response.text

