from random import randint

from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram import F
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from database import database
from keyboard.keyboard import yes_or_no, main_kb


router: Router = Router()
database.sql_start()
memes = database.sql_read_meme()

print(len(memes))
class FSMGetMeme(StatesGroup):
    y_n = State()


@router.message(F.text == "Мемы", StateFilter(default_state))
async def send_meme(message: Message, state: FSMContext):
    indx: int = randint(0, len(memes) - 1)

    await message.answer_photo(memes[indx][0])
    await message.answer("Ещё?", reply_markup=yes_or_no.as_markup(resize_keyboard=True))

    await state.set_state(FSMGetMeme.y_n)


@router.message(StateFilter(FSMGetMeme.y_n))
async def exit_program(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        indx: int = randint(0, len(memes) - 1)
        await message.answer_photo(memes[indx][0])
        await message.answer("Ещё?", reply_markup=yes_or_no.as_markup(resize_keyboard=True))
        return
    elif message.text.lower() == 'нет':
        await message.answer('Шутки кончились😤', reply_markup=main_kb.as_markup(resize_keyboard=True))
        await state.set_state(default_state)
    else:
        await message.answer('Не пон')
