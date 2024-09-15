import google.generativeai as genai
from configs.aicfg import *

def AIGenerate(prompt):
    genai.configure(api_key=KEY)
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)
    return response.text

def AIVision(file, prompt='Реши задачку или пример на фото'):
    file_photo = genai.upload_file(file)
    model = genai.GenerativeModel(MODEL)
    result = model.generate_content(
        [file_photo, '\n\n', prompt]
    )
    return result.text