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
    elif message.text == '☎️Контакты КЦ':
        msg = 'Контакты карьерного центра здесь вы можете обратиться в нужный карьерный центр. Для начала выберите филиал.'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.contacts())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Almaty':
        msg = 'Алматы.\nКанал карьерного центра:\nhttps://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм:@careerstep\n\nТелефон/WhatsApp:+7 771 726 50 38'
        bot.send_message(call.message.chat.id, msg)
    elif call.data == 'Astana':
        msg = 'Астана.\nКанал карьерного центра:\nhttps://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм:@careerstep_astana\n\nТелефон/WhatsApp:+7 777 313 1999'
        bot.send_message(call.message.chat.id, msg)
    elif call.data == 'Karaganda':
        msg = 'Караганла.Канал карьерного центра:https://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм:@Careerstep_krg\n\nТелефон/WhatsApp:+7 708 651 47 62'
        bot.send_message(call.message.chat.id, msg)
bot.polling(none_stop = True)