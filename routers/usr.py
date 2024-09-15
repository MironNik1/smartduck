from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from markups.usr import *
from ai import AIGenerate
from aiogram.fsm.context import FSMContext
from data.user import UserX
from routers.States.usr.State import Task, BuyPRO


router = Router()

@router.message(F.text == '🌎 Профиль')
async def profile(message: Message):
    user = UserX().get_user(message.from_user.id)
    id_user = user[0]
    balance = user[4]
    date = user[1]
    await message.answer(f'🙋‍♂️ Ваш профиль:\n🆔 ID: {id_user}\n💵 Баланс: {balance}$\n📅 Дата регистрации: {date}')

@router.message(F.text == '⬅️ Назад')
async def back(message: Message):
    await message.answer('Главное меню', reply_markup=get_start_kb())

@router.message(F.text == '✨ Получить ответ')
async def get_answer(message: Message, state: FSMContext):
    await message.answer('Введите условие вашей задачи:')
    await state.set_state(Task.task)

@router.message(Task.task)
async def generate_answer(message: Message, state: FSMContext):
    task = message.text
    try:
        answer = AIGenerate(f'Помоги с решением данной задачи по школе:\n{task}.  С полным хорошим и понятным обьяснением')
        await message.answer(f'Ваш ответ: \n\n\n{answer}', reply_markup=like_kb())
        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer('Не могу ответить на ваш вопрос :(', reply_markup=like_kb())

@router.message(F.text == '🌟 Купить PRO')
async def buy_pro(message: Message):
    await message.answer('🌟 Купить PRO', reply_markup=get_back_kb())
    await message.answer('Для чего нужна PRO подписка?\n-Безлимитный доступ к боту, участие в различных конкурсах, доступ в закрытый чат, а также вы можете принять участие в бета-тестировании нашей нейросети WorxAI на 100%(Генерация текста и кода, Помощь с повседневными делами, Генерация красивых изображений, Ответ в текстовом формате, в аудио, а также в формате изображения)\n(Действует скидка 15% на PRO)', reply_markup=payment_kb())
