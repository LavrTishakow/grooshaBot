# .\/.venv/Scripts/activate
import re
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
import logging
# новый импорт!
from aiogram.utils.markdown import hide_link
from aiogram.utils.markdown import hlink
from aiogram.utils.keyboard import InlineKeyboardBuilder
from random import randint
from handlers import questions, different_types


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота


bot = Bot(token="6756665185:AAEFnWozMhj7FTNqIAiyeTv8O8DZ-4LojWw")
dp = Dispatcher(bot=bot)

dp.include_routers(questions.router, different_types.router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
# start


@dp.message(CommandStart(
    deep_link=True,
    magic=F.args.regexp(re.compile(r'book_(\d+)'))
))
async def cmd_start_book(
        message: Message,
        command: CommandObject
):
    book_number = command.args.split("_")[1]
    await message.answer(f"Sending book №{book_number}")
# Запуск процесса поллинга новых апдейтов


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))


# Здесь хранятся пользовательские данные.
# Т.к. это словарь в памяти, то при перезапуске он очистится
user_data = {}


def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr")
        ],
        [types.InlineKeyboardButton(
            text="Подтвердить", callback_data="num_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def update_num_text(message: types.Message, new_value: int):
    await message.edit_text(
        f"Укажите число: {new_value}",
        reply_markup=get_keyboard()
    )


@dp.message(Command("numbers"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())


@dp.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "incr":
        user_data[callback.from_user.id] = user_value+1
        await update_num_text(callback.message, user_value+1)
    elif action == "decr":
        user_data[callback.from_user.id] = user_value-1
        await update_num_text(callback.message, user_value-1)
    elif action == "finish":
        await callback.message.edit_text(f"Итого: {user_value}")

    await callback.answer()

# =============================================================


@dp.message(Command("hidden_link"))
async def cmd_hidden_link(message: Message):
    text = hlink("Документация Telegram: *существует*",
                 "https://telegra.ph/file/562a512448876923e28c3.png")
    await message.answer(text, parse_mode="HTML")


if __name__ == "__main__":
    asyncio.run(main())
