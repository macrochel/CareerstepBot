import telebot, keyboard, db, logging, sys, asyncio, validator
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

#creating database and collection
dblist = db.client.list_database_names()
if "careerBot" not in dblist:
  dbc = db.client['careerBot']
  logger.info("MongoDB status: successfully created database")

collist = dbc.list_collection_names()
if "users" not in collist:
  coll = dbc['users']
  logger.info("MongoDB status: successfully created collection")

#commands handler
@bot.message_handler(commands=['start', 'stuck'])
def command_message(message):
    if message.text == '/start':
        msg = 'Привет, студент!) Я создан для того, чтобы помогать в составление резюме. Я помогу тебе сделать первый шаг в увлекательный мир профессионального развития и карьерного продвижения.'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.menu())
    elif message.text == '/stuck':
        msg = 'Добро пожаловать в меню!'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.menu())

#text handler
@bot.message_handler(content_types=['text'])
def text_message(message):
    if message.text == '📄Создать резюме':
        msg = 'Напиши свое ФИО.\nЖелательно напиши свое ФИО так как в написано у тебя в государственных документах (удостоверение личности).'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.menu())
        bot.register_next_step_handler(message, getName)
    elif message.text == '👤Мой профиль':
        msg = f'id:{message.chat.id}\n\nФИО:\n\n'
        bot.send_message(message.chat.id, msg)
    elif message.text == '☎️Контакты КЦ':
        msg = 'Контакты карьерного центра здесь вы можете обратиться в нужный карьерный центр. Для начала выберите филиал.'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.contacts())

#callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Almaty':
        msg = '🍎Алматы.\n\nКанал карьерного центра:\nhttps://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм: @careerstep\n\nТелефон/WhatsApp: +7 771 726 50 38'
        bot.send_message(call.message.chat.id, msg)
    elif call.data == 'Astana':
        msg = '🌬Астана.\n\nКанал карьерного центра:\nhttps://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм: @careerstep_astana\n\nТелефон/WhatsApp: +7 777 313 19 99'
        bot.send_message(call.message.chat.id, msg)
    elif call.data == 'Karaganda':
        msg = '☀️Караганда.\n\nКанал карьерного центра:\nhttps://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм: @careerstep_krg\n\nТелефон/WhatsApp: +7 708 651 47 62'
        bot.send_message(call.message.chat.id, msg)

#handlers of the steps
def getName(message):
    if message.text != '🏠Вернуться в меню' and message.text != '/stuck' and message.text != '/start':
        msg = 'Напиши свой город, в котором вы ищете работу.'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.nextstep())
        bot.register_next_step_handler(message, getCity)

def getCity(message):
    if message.text != '🏠Вернуться в меню' and message.text != '/stuck' and message.text != '/start':
        msg = 'Загрузите свое фото.\nФото – та деталь, с которой HR начнет знакомство с вами. Не размещайте в своем резюме селфи, мелкие и некачественные фотографии, фото в компании других людей или с общего застолья.\nРекомендации:\n• Остановите выбор на портретном фото или фото в деловом стиле;\n• Выберите нейтральный фон;\n•	Обратите внимание на качество фотографии;\n•	И не забывайте про улыбку – она притягивает внимание и распологает.'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.skipstep())
        bot.register_next_step_handler(message, getPhoto)

def getPhoto(message):
    if message.text != '🏠Вернуться в меню' and message.text != '/stuck' and message.text != '/start':
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = 'storage/pictures/users' + message.photo[1].file_id + '.jpg'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            msg = 'Укажите цель поиска.\nЭто опциональный блок, его не всегда нужно заполнять – все зависит от ваших навыков и вакансии. Если пишите желаемую зарплату, возьмите средний размер оплаты из реальных предложений и прибавьте 10%.\nИсследуйте самостоятельно рынок. Оцените свой опыт работы и посмотрите, в какой ценовой промежуток по зарплате попадаете.\nТак вы сможете узнать, сколько стоит ваша работа, и рассказать ожидания на собеседовании.'
            bot.send_message(message.chat.id, msg, reply_markup=keyboard.skipstep())
            bot.register_next_step_handler(message, getGoal)
        except:
            msg = 'Ошибка при загрузке фото, попробуйте загрузить фото еще раз.'
            bot.send_message(message.chat.id, msg, reply_markup=keyboard.skipstep())
            bot.register_next_step_handler(message, getPhoto)

def getGoal(message):
    if message.text != '🏠Вернуться в меню' and message.text != '/stuck' and message.text != '/start':
        msg = 'Напишите свой номер телефона.\nУкажите актуальный номер телефона, на который вы 100% ответите в рабочее время.'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.nextstep())
        bot.register_next_step_handler(message, getPhone)

def getPhone(message):
    if message.text != '🏠Вернуться в меню' and message.text != '/stuck' and message.text != '/start' and validator.phone(message.text):
        msg = 'Укажите адрес электронный адрес почты.\nИдеальный вариант – это словосочетание фамилии с именем. Если такой нет – заведите специально для рабочих контактов.\nПочта кошечка92 и прочие проявления фантазии рекрутеры не воспринимают всерьез.'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.nextstep())
        bot.register_next_step_handler(message, getEmail)
    elif validator.phone(message.text) != True:
        msg = 'Некорректный формат ввода телефона, вводите номер в формате +7'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.nextstep())
        bot.register_next_step_handler(message, getPhone)

def getEmail(message):
    if message.text != '🏠Вернуться в меню' and message.text != '/stuck' and message.text != '/start' and validator.email(message.text):
        msg = ''
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.nextstep())
        bot.register_next_step_handler(message, getExperience)
    elif validator.email(message.text) != True:
        msg = 'Некорректный формат ввода почты, вводите номер в формате example@gmail.com'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard.nextstep())
        bot.register_next_step_handler(message, getEmail)



#async mailing
async def working(userids, msg):
    while True:
        for userid in userids:
            await bot.send_message(userid, msg)
        await asyncio.sleep(15)

#polling
bot.polling(none_stop = True)
logger.warning("Bot status: stopped")