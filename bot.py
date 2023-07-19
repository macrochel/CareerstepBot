import telebot, keyboard, logging, os
from decouple import config

os.system('clear')

bot = telebot.TeleBot(config('API_KEY'))

f = open('loggs.txt', 'w')
f.close()
logging.basicConfig(filename='loggs.txt',level=logging.INFO, format = '%(asctime)s - %(message)s')
logging.info('Bot started')


@bot.message_handler(commands=['start'])
def command_message(message):
    if message.text == '/start':
        msg = 'Привет, студент!) Я создан для того, чтобы помогать в составление резюме. Я помогу тебе сделать первый шаг в увлекательный мир профессионального развития и карьерного продвижения.'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.menu())

@bot.message_handler(content_types=['text'])
def text_message(message):
    if message.text == '📄Создать резюме':
        msg = 'Напиши свое ФИО.\nЖелательно напиши свое ФИО так как в написано у тебя в государственных документах (удостоверение личности).'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.resume_type())
    

bot.polling(none_stop = True)