from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from markups.usr import *
from ai import AIGenerate, AIVision, AIConversation
from aiogram.fsm.context import FSMContext
from data.user import UserX 
from routers.States.usr.State import *
import os
import asyncio

router = Router()

@router.callback_query(F.data == 'registration')
async def registration(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Хорошо, теперь введи свой возраст:')
    await state.set_state(User.age)

@router.message(User.age)
async def get_age(message: Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)
    async with UserX() as db:
        await db.edit_user(tg_id=message.from_user.id, age=int(age))
    await message.delete()
    await message.answer('Отлично, теперь введи свой гендер:', reply_markup=gender_kb())
    await state.set_state(User.gender)

@router.callback_query(User.gender)
async def get_male(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'male': male = 'Мужской'
    else: male = 'Женский'
    await callback.message.delete()
    await state.update_data(gender=male)
    async with UserX() as db:
        await db.edit_user(tg_id=callback.message.from_user.id, gender=male)
    await callback.message.delete()
    await callback.message.answer('Хорошо, теперь введи своё имя:')
    await callback.answer()
    await state.set_state(User.name)

@router.message(User.name)
async def get_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    async with UserX() as db:
        await db.edit_user(tg_id=message.from_user.id, name=name, isRegistered=True)
    await message.answer_sticker('CAACAgIAAxkBAAEM0QZm6AJoFCsK7GNTzj54X98X7zqDvQACSgIAAladvQrJasZoYBh68DYE')
    await message.delete()
    await message.answer('Отлично, ты успешно зарегистрировался! Теперь у тебя есть доступ к боту!\n(Напиши команду /start для работы с ботом!)', reply_markup=get_start_kb())
    await message.bot.send_message(6910460878, f'Новый пользователь: {message.from_user.username}')
    await state.clear()

@router.message(F.text == '🌎 Профиль')
async def profile(message: Message):
    async with UserX() as db:
        user = await db.get_user(message.from_user.id)
    is_premium = 'Активна' if user[2] else 'Не активна'
    
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
    except Exception as e:
        await state.clear()
        await message.delete()
        await message.answer('Ошибка при взятии фото, попробуйте еще раз!')

@router.callback_query(F.data == 'dislike')
async def like_dislike(callback: CallbackQuery):
    await callback.answer(text='Спасибо за обратную связь. Вы помогли настроить ИИ! ❤️', show_alert=True)

@router.callback_query(F.data == 'like')
async def like_dislike(callback: CallbackQuery):
    await callback.answer(text='Спасибо за обратную связь. Вы помогли настроить ИИ! ❤️', show_alert=True)

@router.callback_query(F.data == 'another_one')
async def another_one(callback: CallbackQuery, state: FSMContext):
    await text_format(callback=callback, state=state)

@router.message(F.text == '🌟 Купить PRO')
async def buy_pro(message: Message):
    await message.answer('🌟 Купить PRO', reply_markup=get_back_kb())
    await message.answer('Для чего нужна PRO подписка?\n-Безлимитный доступ к боту, участие в различных конкурсах, доступ в закрытый чат, а также вы можете принять участие в бета-тестировании нашей нейросети WorxAI на 100%(Генерация текста и кода, Помощь с повседневными делами, Генерация красивых изображений, Ответ в текстовом формате, в аудио, а также в формате изображения)\n(Действует скидка 15% на PRO)', reply_markup=payment_kb())

@router.message(F.text == '🤖 Тест WorxAI')
async def testworxai(message: Message):
    async with UserX() as db:
        user = await db.get_user(message.from_user.id)
    is_premium = user[2]
    if is_premium:
        await message.answer('Выберите действие с нейросетью:', reply_markup=action_with_ai())
    else:
        await message.answer('Выберите действие с нейросетью:', reply_markup=action_with_ai())

@router.message(F.text == '👨🏼‍🏫 Помощь')
async def help(message: Message):
    await message.answer('''
**Добро пожаловать в SmartDuck!**

Ваш бот имеет несколько ключевых функций, которые помогут вам в работе. Вот краткое руководство по тому, как пользоваться ботом:

Основные команды и функции:
Регистрация:

Нажмите на кнопку **"Регистрация"**, чтобы начать процесс регистрации. Вам будет предложено ввести ваш возраст, гендер и имя.
Профиль:

Нажмите на кнопку **"🌎 Профиль"**, чтобы просмотреть свою информацию. Вы увидите ваше имя, возраст, гендер, баланс, статус подписки PRO и дату регистрации.
Получить ответ:

Нажмите на кнопку **"✨ Получить ответ"**, чтобы выбрать способ отправки задания. Вы можете выбрать текстовый формат или отправить изображение с задачей.
Купить PRO:

Нажмите на кнопку **"🌟 Купить PRO"**, чтобы узнать больше о подписке PRO и её преимуществах. Здесь вы можете также сделать покупку и получить доступ к дополнительным функциям.
Тест WorxAI:

Нажмите на кнопку **"🤖 Тест WorxAI"**, чтобы проверить возможности нашей нейросети. Если у вас есть подписка PRO, вы сможете выбрать действие с нейросетью.
Обратная связь:

Нажмите на кнопку **"👍 Нравится"** или **"👎 Не нравится"**, чтобы оставить отзыв и помочь нам улучшить бот.
Отмена действий:

Нажмите на кнопку **"❌ Отмена"**, если хотите отменить текущее действие или задачу.
Примечания:
Поддержка PRO: **Подписка PRO** предоставляет доступ к дополнительным функциям, таким как безлимитный доступ, участие в конкурсах и доступ к закрытому чату. Узнайте больше о подписке на кнопке "🌟 Купить PRO".

Помощь с задачами: Вы можете получить помощь с текстовыми задачами или задачами, связанными с изображениями. Просто выберите соответствующий формат на кнопке "✨ Получить ответ".

Если у вас возникли вопросы или проблемы, не стесняйтесь написать нам. Мы всегда рады помочь!
                         ''', parse_mode='Markdown', reply_markup=get_back_kb())

@router.callback_query(F.data == 'cancel')
async def cancel_solve(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer('Действие отменено')
    await callback.answer()

@router.callback_query(F.data == 'get_dialogue')
async def get_dialogue(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Диалог со мной начался, вы можете закончить в любой момент, нажав на кнопку "Отмена"', reply_markup=otmena_kb())
    await state.set_state(Dialogue.get)
    await callback.answer()

@router.message(F.text == '🛑 Остановить')
async def stop_dialogue(message: Message, state: FSMContext):
    await message.answer('Диалог остановлен')
    await message.delete()
    await state.clear()
    
@router.message(Dialogue.get)
async def dialogue(message: Message, state: FSMContext):
    prompt = message.text
    await message.reply(AIConversation(prompt))

@router.callback_query(F.data == 'top_up')
async def top_up(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите сумму для пополнения баланса (Мин. сумма для пополнения: 1$):', reply_markup=otmena_kb())
    await callback.answer()
    await state.set_state(Top_Up.amount)
    
@router.message(Top_Up.amount)
async def top_up_amount(message: Message, state: FSMContext):
    amount = message.text
    if amount.isdigit() and int(amount) >= 1:
        await message.answer(text='Выберите удобную платежную систему: ', reply_markup=payments_kb())
    else:
        await message.answer('Введите корректную сумму')
