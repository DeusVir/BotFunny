from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from aiogram import Router
from aiogram.fsm.state import default_state, StatesGroup, State

from Handlers.introduction.introduction import FSMIntroduction
from keyboard.keyboard import admin_kb
from lexicon.lexicon import LEXICON
from aiogram.fsm.context import FSMContext


class FSMAdmin(StatesGroup):
    admin = State()


router: Router = Router()


@router.message(Command(commands=['start']), StateFilter(default_state))
async def start_proccess(message: Message, state: FSMContext):
    await message.answer(LEXICON['/start'])
    await state.set_state(FSMIntroduction.name)


@router.message(Command(commands=['help']), StateFilter(default_state))
async def help_proccess(message: Message):
    await message.answer(LEXICON['/help'])


@router.message(Command(commands=['admin']), StateFilter(default_state))
async def start_proccess(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать, хозяин!", reply_markup=admin_kb.as_markup(resize_keyboard=True))
    await state.set_state(FSMAdmin.admin)
