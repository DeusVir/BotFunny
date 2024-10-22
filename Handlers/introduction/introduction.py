from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram import F
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from keyboard.keyboard import yes_or_no, main_kb
from lexicon.lexicon import LEXICON

router: Router = Router()




class FSMIntroduction(StatesGroup):
    name = State()
    y_n = State()


@router.message(StateFilter(FSMIntroduction.name))
async def catch_name(message: Message, state: FSMContext):
    user_name = message.text

    await message.answer(f"{LEXICON['Имя']} {user_name}?", reply_markup=yes_or_no.as_markup(resize_keyboard=True))
    await state.set_state(FSMIntroduction.y_n)


@router.message(StateFilter(FSMIntroduction.y_n))
async def exit_program(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.answer("Отлично! Приступим к работе!", reply_markup=main_kb.as_markup(resize_keyboard=True))
        await state.set_state(default_state)
    elif message.text.lower() == 'нет':
        await message.answer("Что же, так как тебя зовут?", reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSMIntroduction.name)
    else:
        await message.answer("Что сказал?!?")
