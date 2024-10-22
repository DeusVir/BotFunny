from datetime import datetime

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram import Router, types
from aiogram import F
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.state import default_state

import requests
from aiogram.types import ReplyKeyboardRemove
from bs4 import BeautifulSoup

from keyboard.keyboard import yes_or_no, main_kb


class FSMBirthDay(StatesGroup):
    ds = State()


router: Router = Router()


@router.message(F.text == "Гороскоп", StateFilter(default_state))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.reply("Привет! Введите вашу дату рождения в формате ДД.ММ.ГГГГ:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMBirthDay.ds)


@router.message(StateFilter(FSMBirthDay.ds))
async def process_birthday(message: types.Message, state: FSMContext):
    try:

        birth_date = datetime.strptime(message.text, '%d.%m.%Y')
        month = birth_date.month
        day = birth_date.day

        zodiac_sign = get_zodiac_sign(day, month)

        horoscope = get_horoscope(zodiac_sign[1])

        await message.reply(f"Ваш знак зодиака: {zodiac_sign[0]}\n\nГороскоп на сегодня:\n\n{horoscope}",
                            parse_mode=ParseMode.MARKDOWN, reply_markup=main_kb.as_markup(resize_keyboard=True))
        await state.set_state(default_state)
    except ValueError:
        await message.reply("Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.")


# Функция для определения знака зодиака
def get_zodiac_sign(day, month):
    if (month == 1 and day >= 21) or (month == 2 and day <= 19):
        return ["Водолей ♒", "Aquarius"]
    elif (month == 2 and day >= 20) or (month == 3 and day <= 20):
        return ["Рыбы ♓", "Pisces"]
    elif (month == 3 and day >= 21) or (month == 4 and day <= 20):
        return ["Овен ♈", "Aries"]
    elif (month == 4 and day >= 21) or (month == 5 and day <= 20):
        return ["Телец ♉ ", "Taurus"]
    elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
        return ["Близнецы ♊", "Gemini"]
    elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
        return ["Рак ♋", "Cancer"]
    elif (month == 7 and day >= 23) or (month == 8 and day <= 23):
        return ["Лев ♌", "Leo"]
    elif (month == 8 and day >= 24) or (month == 9 and day <= 23):
        return ["Дева ♍", "Virgo"]
    elif (month == 9 and day >= 24) or (month == 10 and day <= 23):
        return ["Весы ♎", "Libra"]
    elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
        return ["Скорпион ♏", "Scorpio"]
    elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
        return ["Стрелец ♐", "sagittarius"]
    elif (month == 12 and day >= 22) or (month == 1 and day <= 20):
        return ["Козерог ♑", "Capricorn"]


# Функция для получения гороскопа
def get_horoscope(zodiac_sign):
    url = f"https://horo.mail.ru/prediction/{zodiac_sign.lower()}/today/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        horoscope_div = soup.find('div', attrs={'article-item-type': 'html'})
        if horoscope_div:
            horoscope_text = '\n'.join([p.text.strip() for p in horoscope_div.find_all('p')])
            return horoscope_text
        else:
            return "Не удалось найти div с гороскопом."
    else:
        return "Не удалось получить гороскоп. Попробуйте позже."
