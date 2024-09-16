from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart
from configs.botcfg import TOKEN
from markups.usr import registration_kb, get_start_kb
from routers.usr import router as usr
from data.user import UserX
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio
import sys
import logging


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_routers(usr)

@dp.message(CommandStart())
async def on_main(message: types.Message):
    async with UserX() as db:
        try:
            await db.create_user(tg_id=message.from_user.id)
        except Exception as e:
            print(f'User already exists or {e}')

        user = await db.get_user(tg_id=message.from_user.id)
        if not user[8]: 
            await message.answer(
                text=f'Добро пожаловать в SmartDuck {message.from_user.full_name}!\nДля работы с ботом необходимо пройти регистрацию\n', 
                reply_markup=registration_kb()
            )
        else:
            await message.answer(
                text=f'Привет снова! {user[7]}!',
                reply_markup=get_start_kb()
            )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
