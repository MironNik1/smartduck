from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class User(StatesGroup):
    age = State()
    gender = State()
    name = State()

class Text(StatesGroup):
    get = State()

class Photo(StatesGroup):
    get = State()

class BuyPRO(StatesGroup):
    buy = State()

class Top_Up(StatesGroup):
    amount = State()
    
class Dialogue(StatesGroup):
    get = State()