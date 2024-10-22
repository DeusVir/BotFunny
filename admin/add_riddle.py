from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram import Router, F
from database.database import  sql_add_riddle
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from Handlers.usual_commands import FSMAdmin
from keyboard.keyboard import yes_or_no, main_kb


class FSMRiddle(StatesGroup):
    send_riddle = State()
    send_answer = State()
    y_n = State()


router: Router = Router()

riddle = {}


@router.message(F.text == "Добавить загадку", StateFilter(FSMAdmin.admin))
async def admin(message: Message, state: FSMContext):
    await message.answer('Введите фотографию.', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMRiddle.send_riddle)


@router.message(FSMRiddle.send_riddle)
async def getRiddle(message: Message, state: FSMContext):
    if message.text is not None:
        await message.answer('Отправь фотографию.')
        return
    else:
        riddle['img'] = message.photo[0].file_id
    await  message.answer('Введите ответ.', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMRiddle.send_answer)


@router.message(FSMRiddle.send_answer)
async def getRiddleAnswer(message: Message, state: FSMContext):

    riddle['answer'] = message.text
    await sql_add_riddle(riddle)
    await message.answer('Хотите добавить еще загадку?', reply_markup=yes_or_no.as_markup(resize_keyboard=True))

    await state.set_state(FSMRiddle.y_n)

@router.message(StateFilter(FSMRiddle.y_n))
async def exit_program(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.answer('Введите фото')
        await state.set_state(FSMRiddle.send_riddle)
    elif message.text.lower() == 'нет':
        await message.answer('Пока, хозяин!',reply_markup=main_kb.as_markup(resize_keyboard=True))
        await state.set_state(default_state)
    else:
        await message.answer('Напишите да или нет.')
