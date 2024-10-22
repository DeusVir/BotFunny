from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram import Router, F
from database.database import  sql_add_anecdote
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from Handlers.usual_commands import FSMAdmin
from keyboard.keyboard import yes_or_no, main_kb


class FSMAnecdote(StatesGroup):
    send_anecdote = State()
    y_n = State()


router: Router = Router()

anecdote = {}


@router.message(F.text == "Добавить анекдот", StateFilter(FSMAdmin.admin))
async def admin(message: Message, state: FSMContext):
    await message.answer('Введите анекдот', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMAnecdote.send_anecdote)


@router.message(FSMAnecdote.send_anecdote)
async def getAnecdote(message: Message, state: FSMContext):

    anecdote['joke'] = message.text
    await sql_add_anecdote(anecdote)

    await message.answer('Хотите добавить еще анекдот?', reply_markup=yes_or_no.as_markup(resize_keyboard=True))
    await state.set_state(FSMAnecdote.y_n)


@router.message(StateFilter(FSMAnecdote.y_n))
async def exit_program(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.answer('Введите анекдот')
        await state.set_state(FSMAnecdote.send_anecdote)
    elif message.text.lower() == 'нет':
        await message.answer('Пока, хозяин!', reply_markup=main_kb.as_markup(resize_keyboard=True))
        await state.set_state(default_state)
    else:
        await message.answer('Напишите да или нет.')
