from random import randint

from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram import F
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from database import database
from keyboard.keyboard import yes_or_no, main_kb

router: Router = Router()
database.sql_start()
riddles = database.sql_read_riddle()

mas: list = [0]


class FSMGetRiddles(StatesGroup):
    guessing = State()
    lose = State()
    y_n = State()


@router.message(F.text == 'Загадки', StateFilter(default_state))
async def send_riddle(message: Message, state: FSMContext):
    indx: int = randint(0, len(riddles) - 1)
    mas[0] = indx
    await message.answer_photo(riddles[indx][0], reply_markup=ReplyKeyboardRemove())

    await state.set_state(FSMGetRiddles.guessing)


@router.message(StateFilter(FSMGetRiddles.guessing))
async def get_answer(message: Message, state: FSMContext):
    if message.text.lower() == riddles[mas[0]][1]:
        await message.answer("Абсолютно верно! Хотите ещё?", reply_markup=yes_or_no.as_markup(resize_keyboard=True))
        await state.set_state(FSMGetRiddles.y_n)
    else:
        await message.answer("Неправильно. Сдаетесь?", reply_markup=yes_or_no.as_markup(resize_keyboard=True))
        await state.set_state(FSMGetRiddles.lose)


@router.message(StateFilter(FSMGetRiddles.lose))
async def exit_or_not(message: Message, state: FSMContext):
    if message.text.lower() == 'да':

        await message.answer(f"Эх ты... Правильный ответ - {riddles[mas[0]][1]}.")
        await message.answer("Ну что, еще загадку?", reply_markup=yes_or_no.as_markup(resize_keyboard=True))
        await state.set_state(FSMGetRiddles.y_n)
        return
    elif message.text.lower() == 'нет':
        await message.answer('Думайте.', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSMGetRiddles.guessing)
    else:
        await message.answer('Не пон')


@router.message(StateFilter(FSMGetRiddles.y_n))
async def exit_program(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        indx: int = randint(0, len(riddles) - 1)
        mas[0] = indx
        await message.answer_photo(riddles[indx][0], reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSMGetRiddles.guessing)
        return
    elif message.text.lower() == 'нет':

        await message.answer(f'Куда есть вход, а выхода нет?',
                             reply_markup=main_kb.as_markup(resize_keyboard=True))
        await state.set_state(default_state)
    else:
        await message.answer('Не пон')
