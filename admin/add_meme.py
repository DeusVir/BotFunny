from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram import Router, F
from database.database import sql_add_meme
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from Handlers.usual_commands import FSMAdmin
from keyboard.keyboard import yes_or_no, main_kb


class FSMMeme(StatesGroup):
    send_meme = State()
    y_n = State()


router: Router = Router()

meme = {}


@router.message(F.text == "Добавить мем", StateFilter(FSMAdmin.admin))
async def admin(message: Message, state: FSMContext):
    await message.answer('Введите фотографию.', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMMeme.send_meme)


@router.message(FSMMeme.send_meme)
async def getMeme(message: Message, state: FSMContext):
    if message.text is not None:
        await message.answer('Отправь фотографию.')
        return
    else:
        meme['meme'] = message.photo[0].file_id
        await sql_add_meme(meme)
    await message.answer('Хотите добавить еще мемчик?', reply_markup=yes_or_no.as_markup(resize_keyboard=True))
    await state.set_state(FSMMeme.y_n)


@router.message(StateFilter(FSMMeme.y_n))
async def exit_program(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.answer('Введите фото')
        await state.set_state(FSMMeme.send_meme)
    elif message.text.lower() == 'нет':
        await message.answer('Пока, хозяин!',reply_markup=main_kb.as_markup(resize_keyboard=True))
        await state.set_state(default_state)
    else:
        await message.answer('Напишите да или нет.')
