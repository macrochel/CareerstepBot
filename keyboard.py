from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def menu():
	menu_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	button1 = types.KeyboardButton('📄Создать резюме')
	button2 = types.KeyboardButton('☎️Контакты КЦ')
	button3 = types.KeyboardButton('⚙️Настройки')
	menu_keyboard.add(button1)
	menu_keyboard.add(button2, button3)
	return menu_keyboard