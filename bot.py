import telebot, keyboard, db, logging, sys
from decouple import config

bot = telebot.TeleBot(config('API_KEY'))

#logging into console
logger = logging.getLogger("logger")
logger.setLevel(level=logging.DEBUG)
logStreamFormatter = logging.Formatter(
  fmt=f"%(levelname)s %(asctime)s - %(message)s", 
  datefmt="%H:%M:%S"
)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter(logStreamFormatter)
consoleHandler.setLevel(level=logging.DEBUG)
logger.addHandler(consoleHandler)

#logging into .log file
logFileFormatter = logging.Formatter(
    fmt=f"%(levelname)s %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
fileHandler = logging.FileHandler(filename='.log')
fileHandler.setFormatter(logFileFormatter)
fileHandler.setLevel(level=logging.INFO)
logger.addHandler(fileHandler)

try:
    logger.info("Bot status: working")
    db.client.admin.command('ping')
    logger.info("Bot status: successfully connected to MongoDB")
except Exception as e:
    logger.error(e)
    logger.error("Bot status: crashed with error - unsuccessfully connected to MongoDB")

#commands handler
@bot.message_handler(commands=['start', 'stuck'])
def command_message(message):
    if message.text == '/start':
        msg = 'Привет, студент!) Я создан для того, чтобы помогать в составление резюме. Я помогу тебе сделать первый шаг в увлекательный мир профессионального развития и карьерного продвижения.'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.menu())
    elif message.text == '/stuck':
        msg = 'Я вернул тебя в меню!'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.menu())

#text handler
@bot.message_handler(content_types=['text'])
def text_message(message):
    if message.text == '📄Создать резюме':
        msg = 'Напиши свое ФИО.\nЖелательно напиши свое ФИО так как в написано у тебя в государственных документах (удостоверение личности).'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.resume_type())
        bot.register_next_step_handler(message, getName)
    elif message.text == '☎️Контакты КЦ':
        msg = 'Контакты карьерного центра здесь вы можете обратиться в нужный карьерный центр. Для начала выберите филиал.'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.contacts())

#callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Almaty':
        msg = 'Алматы.\n\nКанал карьерного центра:\nhttps://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм: @careerstep\n\nТелефон/WhatsApp: +7 771 726 50 38'
        bot.send_message(call.message.chat.id, msg)
    elif call.data == 'Astana':
        msg = 'Астана.\n\nКанал карьерного центра:\nhttps://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм: @careerstep_astana\n\nТелефон/WhatsApp: +7 777 313 19 99'
        bot.send_message(call.message.chat.id, msg)
    elif call.data == 'Karaganda':
        msg = 'Караганда.\n\nКанал карьерного центра:\nhttps://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм: @careerstep_krg\n\nТелефон/WhatsApp: +7 708 651 47 62'
        bot.send_message(call.message.chat.id, msg)

#handlers of the steps
def getName(message):
    if message.text != 'Меню':
        msg = 'Напиши свой город, в котором вы ищете работу.'
        bot.send_message(message.chat.id, msg)
        bot.register_next_step_handler(message, getCity)

def getCity(message):
    if message.text != 'Меню':
        msg = 'Загрузите свое фото.\nФото – та деталь, с которой HR начнет знакомство с вами. Не размещайте в своем резюме селфи, мелкие и некачественные фотографии, фото в компании других людей или с общего застолья.\nРекомендации:\n•Остановите выбор на портретном фото или фото в деловом стиле;\n•  Выберите нейтральный фон;\n•	Обратите внимание на качество фотографии;\n•	И не забывайте про улыбку – она притягивает внимание и распологает.'
        bot.send_message(message.chat.id, msg)

#polling
bot.polling(none_stop = True)
logger.warning("Bot status: stopped")