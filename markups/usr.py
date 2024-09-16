from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def get_start_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text='🌎 Профиль'))
    kb.row(KeyboardButton(text='✨ Получить ответ'), KeyboardButton(text='🌟 Купить PRO'))
    kb.row(KeyboardButton(text='👨🏼‍🏫 Помощь'), KeyboardButton(text='🤖 Тест WorxAI'))
    return kb.as_markup(resize_keyboard=True)

def get_back_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text='⬅️ Назад'))
    return kb.as_markup(resize_keyboard=True)

def get_buy_pro_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Купить PRO (навсегда = 10$)', callback_data='buy_subscrition'))
    return kb.as_markup()

def like_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='👍🏻', callback_data='like'))
    kb.add(InlineKeyboardButton(text='👎🏻', callback_data='dislike'))
    return kb.as_markup(max_width=1)

def payment_kb():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Купить на 1 день', callback_data='1day'))
    kb.row(InlineKeyboardButton(text='Купить на 7 дней', callback_data='7day'))
    kb.row(InlineKeyboardButton(text='Купить на 30 дней', callback_data='30day'))
    kb.row(InlineKeyboardButton(text='Купить навсгда', callback_data='permanent'))
    return kb.as_markup(max_width=1)

def action_solve():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Отправить текст', callback_data='text'))
    kb.add(InlineKeyboardButton(text='Отправить фото', callback_data='photo'))

    return kb.as_markup()

def otmena_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='🚫 Отменить', callback_data='cancel'))
    return kb.as_markup()

def action_with_ai():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Общение', callback_data='get_dialogue'))
    kb.add(InlineKeyboardButton(text='Генерация текста', callback_data='get_help'))
    kb.row(InlineKeyboardButton(text='Генерация кода', callback_data='get_code'))
    kb.row(InlineKeyboardButton(text='Генерация изображения', callback_data='get_image'))
    return kb.as_markup()

def profile_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Пополнить баланс', callback_data='top_up'))
    kb.add(InlineKeyboardButton(text='Настройки', callback_data='settings'))
    kb.row(InlineKeyboardButton(text='Связь с тех. поддержкой', callback_data='help_me'))
    return kb.as_markup()

def registration_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Зарегистрироваться', callback_data='registration'))
    return kb.as_markup()

def payments_kb():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='CryptoBot', callback_data='cryptobot'))
    kb.row(InlineKeyboardButton(text='AAiO', callback_data='aaio'))
    kb.row(InlineKeyboardButton(text='Click Uzbekistan', callback_data='click'))
    kb.row(InlineKeyboardButton(text='YooMoney', callback_data='yoomoney'))
    return kb.as_markup