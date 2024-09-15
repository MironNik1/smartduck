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
    kb.row(InlineKeyboardButton(text='Оплатить с баланса', callback_data='pay_from_balance'))
    kb.row(InlineKeyboardButton(text='Оплатить через AAIO(СПб, карта, и тд)', callback_data='pay_by_RUcard'))
    kb.row(InlineKeyboardButton(text='Оплатить с CryptoBot', callback_data='pay_by_send'))
    kb.row(InlineKeyboardButton(text='Оплатить с ClickUZ', callback_data='pay_by_click'))
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