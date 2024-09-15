from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class Text(StatesGroup):
    get = State()

class Photo(StatesGroup):
    get = State()

class BuyPRO(StatesGroup):
    buy = State()
