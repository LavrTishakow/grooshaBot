from aiogram import Router, F
from aiogram.types import Message
from random import choice


router = Router()


@router.message(F.text)
async def greet_alice(message: Message):
    # print("Хэндлер для Алисы")
    phrases = [
        "Привет, {name}. Ты сегодня красотка!",
        "Ты самая умная, {name}",
    ]
    if message.from_user.id == 111:
        await message.answer(
            choice(phrases).format(name="аье5лдю с Алиса")
        )


@router.message(F.text)
async def greet_bob(message: Message):
    phrases = [
        "Привет, {name}. Ты самый сильный!",
        "Ты крут, {name}!",
    ]
    if message.from_user.id == 777:
        await message.answer(
            choice(phrases).format(name="Боб")
        )


@router.message(F.text)
async def stranger_go_away(message: Message):
    if message.from_user.id not in (111, 777):
        await message.answer("Я с тобой не разговариваю!")


@router.message(F.sticker)
async def message_with_sticker(message: Message):
    await message.answer("Это стикер!")


@router.message(F.animation)
async def message_with_gif(message: Message):
    await message.answer("Это GIF!")
