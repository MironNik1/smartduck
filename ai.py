import google.generativeai as genai
from configs.aicfg import *

def AIGenerate(prompt):
    genai.configure(api_key=KEY)
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)
    return response.text

def AIVision(file, prompt='Реши задачку или пример или ответь на вопросы на фото с подробным объяснением'):
    genai.configure(api_key=KEY)
    file_photo = genai.upload_file(file)
    model = genai.GenerativeModel(MODEL)
    result = model.generate_content(
        [file_photo, '\n\n', prompt]
    )
    return result.text

def AIConversation(prompt):
    genai.configure(api_key=KEY)
    model = genai.GenerativeModel(MODEL)
    conversation = model.start_chat()
    response = conversation.send_message(f'{prompt},( на вопрос кто ты и подобные отвечай что ты Worx AI)', stream=True)
    return response.text