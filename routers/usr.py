from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from markups.usr import *
from ai import AIGenerate, AIVision
from aiogram.fsm.context import FSMContext
from data.user import UserX
from routers.States.usr.State import Text, Photo, BuyPRO, User
from PIL import Image
from configs.botcfg import TOKEN as API_TOKEN

import os

router = Router()

@router.message(F.data == 'registration')
async def registration(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Хорошо, теперь введи свой возраст:')
    await state.set_state(User.age)

@router.message(User.age)
async def get_age(message: Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)
    UserX().edit_user(tg_id=message.from_user.id, age=int(age))
    await message.answer('Отлично, теперь введи свой гендер:')
    await state.set_state(User.gender)

@router.message(User.gender)
async def get_male(message: Message, state: FSMContext):
    male = message.text
    await state.update_data(gender=male)
    UserX().edit_user(tg_id=message.from_user.id, gender=male)
    await message.answer('Хорошо, теперь введи своё имя:')
    await state.set_state(User.name)
    
@router.message(User.name)
async def get_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    UserX().edit_user(tg_id=message.from_user.id, name=name, isRegistered = True)
    await message.answer_sticker('CAACAgIAAxkBAAEM0QZm6AJoFCsK7GNTzj54X98X7zqDvQACSgIAAladvQrJasZoYBh68DYE')
    await message.answer('Отлично, ты успешно зарегистрировался! Теперь у тебя есть доступ к боту!\n(Напиши команду /start для работы с ботом!)')
    await state.clear()

@router.message(F.text == '🌎 Профиль')
async def profile(message: Message):
    user = UserX().get_user(message.from_user.id)
    is_premium = user[2]
    if is_premium == True:
        is_premium = 'Активна'
    else: is_premium = 'Не активна'
    
    id_user = user[0]
    balance = user[4]
    date = user[1]
    name = user[7]
    age = user[5]
    gender = user[6]
    await message.answer(f'🙋‍♂️ Ваш профиль:\n🆔 ID: {id_user},\n🙋‍♂️ Имя: {name}\n☘️ Возраст: {age}\n👫 Гендер:{gender}\n💵 Баланс: {balance}$\n✨ PRO подписка: {is_premium} \n📅 Дата регистрации: {date}', reply_markup=profile_kb())

@router.message(F.text == '⬅️ Назад')
async def back(message: Message):
    await message.answer('Главное меню', reply_markup=get_start_kb())

@router.message(F.text == '✨ Получить ответ')
async def get_answer(message: Message, state: FSMContext):
    await message.answer('Выберите способ отправки задания:', reply_markup=action_solve())

@router.callback_query(F.data == 'text')
async def text_format(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите условие задачи:', reply_markup=otmena_kb())
    await callback.answer()
    await state.set_state(Text.get)

@router.message(Text.get)
async def generate_answer(message: Message, state: FSMContext):
    await message.reply('👨🏻‍🏫 Генерирую ответ...')
    task = message.text
    try:
        answer = AIGenerate(f'Помоги с решением данной задачи по школе:\n{task}.  С полным хорошим и понятным обьяснением')
        await message.answer(f'Ваш ответ: \n\n\n{answer}', reply_markup=like_kb(), parse_mode='Markdown')
        await state.clear()

    except Exception as e:
        await state.clear()
        await message.answer(f'Не могу ответить на ваш вопрос :(\n\n({e})', reply_markup=like_kb())
        await message.delete()

@router.callback_query(F.data == 'photo')
async def get_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Отправьте изображение вашей задачи:', reply_markup=otmena_kb())
    await callback.answer()
    await state.set_state(Photo.get)

@router.message(Photo.get)
async def handle_photo(message: Message, bot: Bot, state: FSMContext):
    await message.reply('👨🏻‍🏫 Генерирую ответ...')
    try:
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        await bot.download(file=file_info, destination='photo.jpg')


        answer = AIVision(file='photo.jpg')
        await message.answer(f'Ваш ответ: \n\n\n{answer}', reply_markup=like_kb())
        await state.clear()

        
        os.remove('photo.jpg')
    except:
        await state.clear()
        await message.delete()
        await message.answer('Ошибка при взятии фото, попробуйте еще раз!')


@router.callback_query(F.data == 'dislike')
async def like_dislike(callback: CallbackQuery):
    await callback.answer(text='Спасибо за обратную связь. Вы помогли настроить ИИ! ❤️', show_alert=True)
    
@router.callback_query(F.data == 'like')
async def like_dislike(callback: CallbackQuery):
    await callback.answer(text='Спасибо за обратную связь. Вы помогли настроить ИИ! ❤️', show_alert=True)

@router.message(F.text == '🌟 Купить PRO')
async def buy_pro(message: Message):
    await message.answer('🌟 Купить PRO', reply_markup=get_back_kb())
    await message.answer('Для чего нужна PRO подписка?\n-Безлимитный доступ к боту, участие в различных конкурсах, доступ в закрытый чат, а также вы можете принять участие в бета-тестировании нашей нейросети WorxAI на 100%(Генерация текста и кода, Помощь с повседневными делами, Генерация красивых изображений, Ответ в текстовом формате, в аудио, а также в формате изображения)\n(Действует скидка 15% на PRO)', reply_markup=payment_kb())

@router.message(F.text == '🤖 Тест WorxAI')
async def testworxai(message: Message):
    is_premium = UserX.get_user(message.from_user.id)[2]
    if is_premium == True:
        await message.answer('Выберите действие с нейросетью:', reply_markup=action_with_ai())
    else: await message.answer('У вас нет PRO подписки', reply_markup=get_back_kb())

@router.callback_query(F.data == 'cancel')
async def cancel_solve(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer('Действие отменено')
    await callback.answer()
    
@router.callback_query(F.data == 'get_dialogue')
async def get_dialogue(callback: CallbackQuery):
    await callback.message.answer('Введите ваш вопрос:', reply_markup=otmena_kb())
    await callback.answer()

