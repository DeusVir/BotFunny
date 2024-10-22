from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

buttons1: list[KeyboardButton] = [KeyboardButton(text='Да'), KeyboardButton(text='Нет') ]
yes_or_no: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
yes_or_no.row(*buttons1)


buttons2: list[KeyboardButton] = [KeyboardButton(text='Анекдоты'), KeyboardButton(text='Загадки'),
                                  KeyboardButton(text='Истории'),KeyboardButton(text='Мемы'),KeyboardButton(text='Гороскоп'),
                                  KeyboardButton(text='Кликер')]
main_kb: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

main_kb.row(buttons2[0], buttons2[1], buttons2[2])
main_kb.row(buttons2[3], buttons2[4], buttons2[5])

buttons3: list[KeyboardButton] = [KeyboardButton(text='Добавить мем'),KeyboardButton(text='Добавить анекдот')
    ,KeyboardButton(text='Добавить загадку')]
admin_kb: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
admin_kb.row(*buttons3)