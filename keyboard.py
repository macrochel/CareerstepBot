from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def menu():
	menu_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	button1 = types.KeyboardButton('📄Создать резюме')
	button2 = types.KeyboardButton('👤Мой профиль')
	button3 = types.KeyboardButton('☎️Контакты КЦ')
	menu_keyboard.add(button1)
	menu_keyboard.add(button2, button3)
	return menu_keyboard

def contacts():
	contacts_keyboard = types.InlineKeyboardMarkup(row_width=3)
	button1 = types.InlineKeyboardButton('🍎Алматы', callback_data='Almaty')
	button2 = types.InlineKeyboardButton('🌬Астана', callback_data='Astana')
	button3 = types.InlineKeyboardButton('☀️Караганда.', callback_data='Karaganda')
	contacts_keyboard.add(button1, button2, button3)
	return contacts_keyboard

def firststep():
	firststep_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button1 = types.KeyboardButton('🏠Вернуться в меню')
	firststep_keyboard.add(button1)
	return firststep_keyboard

def nextstep():
	nextstep_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	button1 = types.KeyboardButton('🔙Вернуться на прошлый шаг')
	button2 = types.KeyboardButton('🏠Вернуться в меню')
	nextstep_keyboard.add(button1)
	nextstep_keyboard.add(button2)
	return nextstep_keyboard

def skipstep():
	nextstep_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	button1 = types.KeyboardButton('🔙Вернуться на прошлый шаг')
	button2 = types.KeyboardButton('🔜Пропустить шаг')
	button3 = types.KeyboardButton('🏠Вернуться в меню')
	nextstep_keyboard.add(button1, button2)
	nextstep_keyboard.add(button3)
	return nextstep_keyboard