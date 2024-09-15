from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class Task(StatesGroup):
    task = State()

class BuyPRO(StatesGroup):
    buy = State()