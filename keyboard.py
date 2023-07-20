from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

def menu():
	menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	button1 = KeyboardButton('📄Создать резюме')
	button2 = KeyboardButton('👤Мой профиль')
	button3 =  KeyboardButton('☎️Контакты КЦ')
	menu_keyboard.add(button1)
	menu_keyboard.add(button2, button3)
	return menu_keyboard

def contacts():
	contacts_keyboard =  InlineKeyboardMarkup(row_width=3)
	button1 = InlineKeyboardButton('🍎Алматы', callback_data='Almaty')
	button2 = InlineKeyboardButton('🌬Астана', callback_data='Astana')
	button3 = InlineKeyboardButton('☀️Караганда.', callback_data='Karaganda')
	contacts_keyboard.add(button1, button2, button3)
	return contacts_keyboard

def firststep():
	firststep_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button1 = KeyboardButton('🏠Вернуться в меню')
	firststep_keyboard.add(button1)
	return firststep_keyboard

def nextstep():
	nextstep_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	button1 = KeyboardButton('🔙Вернуться на прошлый шаг')
	button2 = KeyboardButton('🏠Вернуться в меню')
	nextstep_keyboard.add(button1)
	nextstep_keyboard.add(button2)
	return nextstep_keyboard

def skipstep():
	skipstep_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	button1 = KeyboardButton('🔙Вернуться на прошлый шаг')
	button2 = KeyboardButton('Пропустить шаг🔜')
	button3 = KeyboardButton('🏠Вернуться в меню')
	skipstep_keyboard.add(button1, button2)
	skipstep_keyboard.add(button3)
	return skipstep_keyboard

def noexpirience():
	noexpirience_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	button1 = KeyboardButton('🔙Вернуться на прошлый шаг')
	button2 = KeyboardButton('Нет опыта работы❔')
	button3 = KeyboardButton('🏠Вернуться в меню')
	noexpirience_keyboard.add(button1, button2)
	noexpirience_keyboard.add(button3)
	return noexpirience_keyboard