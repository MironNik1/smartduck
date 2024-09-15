from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart
from configs.botcfg import *
from markups.usr import *
from routers.usr import router as usr
from data.user import UserX

import asyncio, sys, logging


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_routers(usr)

@dp.message(CommandStart())
async def onMain(message: types.Message):
    db = UserX(db_file='db_users.sql')
    try:
        db.create_user(tg_id=message.from_user.id)
    except Exception as e: print(f'User already exists or {e}')
    finally:
        await message.answer_sticker('CAACAgIAAxkBAAEMxFVm2kB3I7nri4tIgUe33ICbSjII9wACAQEAAladvQoivp8OuMLmNDYE')
        await message.answer(f"Привет {message.from_user.full_name}!", reply_markup=get_start_kb())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())