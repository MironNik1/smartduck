from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class Task(StatesGroup):
    photo = State()
    text = State()

class BuyPRO(StatesGroup):
    buy = State()