import telebot, logging, db, pdf
from keyboard import firststep, firststep_inline, nextstep, skipstep, noexpirience, menu, contacts, profile
from sys import stdout
from os import path as pather
from os import remove
from decouple import config
from validator import phone, email

bot = telebot.TeleBot(config("API_KEY"))

filterList = ["/start", "/stuck", "🏠Вернуться в меню", "Нет опыта работы❔", "⬅️Вернуться на прошлый шаг", "Пропустить шаг➡️"]
stepList = ["⬅️Вернуться на прошлый шаг", "Пропустить шаг➡️"]

#logging into console
logger = logging.getLogger("logger")
logger.setLevel(level=logging.DEBUG)
logStreamFormatter = logging.Formatter(
  fmt=f"%(levelname)s %(asctime)s - %(message)s", 
  datefmt="%H:%M:%S"
)
consoleHandler = logging.StreamHandler(stream=stdout)
consoleHandler.setFormatter(logStreamFormatter)
consoleHandler.setLevel(level=logging.DEBUG)
logger.addHandler(consoleHandler)

#logging into .log file
logFileFormatter = logging.Formatter(
    fmt=f"%(levelname)s %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
fileHandler = logging.FileHandler(filename="storage/loggs/.log")
fileHandler.setFormatter(logFileFormatter)
fileHandler.setLevel(level=logging.INFO)
logger.addHandler(fileHandler)

try:
    logger.info("{Bot status}: working")
    dbc, coll = db.init()
    logger.info("{Bot status}: successfully connected to MongoDB")
    logger.info("{MongoDB status}: successfully connected database")
except Exception as e:
    logger.error("{Bot status}: crashed with error - unsuccessfully connected to MongoDB")
    logger.error(e)

#commands handler
@bot.message_handler(commands=["start", "stuck"])
def command_message(message):
    if message.text == "/start":
        msg = "Привет, студент!) Я создан для того, чтобы помогать в составление резюме. Я помогу тебе сделать первый шаг в увлекательный мир профессионального развития и карьерного продвижения."
        sendCaptionPhoto(message.chat.id, 1, msg, menu())
        x = db.initUser(coll, message)
        logger.debug(x)
    elif message.text == "/stuck":
        goHome(message)

#text handler
@bot.message_handler(content_types=["text"])
def text_message(message):
    if message.text == "📄Создать резюме":
        if db.findUser(coll, message) != None:
            msg = "Ты уже создал резюме, хочешь его обновить?"
            bot.send_message(message.chat.id, msg, reply_markup=firststep_inline())
        else:
            msg = "Напиши свое ФИО.\n\nЖелательно напиши свое ФИО так как в написано у тебя в государственных документах (удостоверение личности)."
            sendCaptionPhoto(message.chat.id, 2, msg, firststep())
            bot.register_next_step_handler(message, getName)
    elif message.text == "👤Мой профиль":
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEJwSBkucJChvEVOe95t_Dl9OxPsGLeHwACQC8AAlxayEm6phyX7-7aXi8E")
        user = db.findUser(coll, message)
        if user != None:
            msg = f"📟id: {message.chat.id},\n👤ФИО: {user['name']}\n🌇Город: {user['city']}\n🎯Цель: {user['goal']}\n📱Номер телефона: {user['phone']}\n✉️Почта: {user['email']}\n🎓Образование: {user['education']}\n💡Опыт: {user['expierence']}\n🔧Hard skills: {user['hardSkills']}\n🗣Soft skills: {user['softSkills']}\n🗂Дополнительная информация: {user['addInfo']}"
            bot.send_message(message.chat.id, msg, reply_markup=profile())
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEJwYBkugieMYaSy1dDSIJhKy2gZj7VsAACgSwAAs7w0Elawcv8qxYc3C8E")
        
    elif message.text == "☎️Контакты КЦ":
        msg = "Контакты карьерного центра здесь вы можете обратиться в нужный карьерный центр. Для начала выберите филиал."
        sendCaptionPhoto(message.chat.id, 3, msg, contacts())
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEJwYRkugurwYlWoZrZCmy7O7uu7ob4KAACNDAAAlaN0Ul6sq0rDm2q8S8E")
    elif message.text == "🏠Вернуться в меню":
        goHome(message)
    elif message.text == "✅Да":
        msg = "Напиши свое ФИО.\n\nЖелательно напиши свое ФИО так как в написано у тебя в государственных документах (удостоверение личности)."
        sendCaptionPhoto(message.chat.id, 2, msg, firststep())
        bot.register_next_step_handler(message, getName)

#callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "Almaty":
        msg = "🍎Алматы\n\nКанал карьерного центра:\nhttps://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм: @careerstep\n\nТелефон/WhatsApp: +7 771 726 50 38"
        sendCaptionPhoto(call.message.chat.id, 4, msg, menu())
    elif call.data == "Astana":
        msg = "🌬Астана\n\nКанал карьерного центра:\nhttps://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм: @careerstep_astana\n\nТелефон/WhatsApp: +7 777 313 19 99"
        sendCaptionPhoto(call.message.chat.id, 5, msg, menu())
    elif call.data == "Karaganda":
        msg = "☀️Караганда\n\nКанал карьерного центра:\nhttps://t.me/+M-FBa3ByjddmYTIy\n\nТелеграм: @careerstep_krg\n\nТелефон/WhatsApp: +7 708 651 47 62"
        sendCaptionPhoto(call.message.chat.id, 6, msg, menu())
    elif call.data == "create_resume":
        generateResume(call.message)

#functions 
def goHome(message):
        msg = "Добро пожаловать в меню!"
        bot.send_message(message.chat.id, msg, reply_markup=menu())

def sendCaptionPhoto(chatid, number, msg, keyboard):
    path = "storage/pictures/" + str(number) + ".PNG"
    if not pather.exists(path):
        bot.send_message(chatid, "Фото не найдено")
        return
    with open(path, "rb") as photo:
        bot.send_photo(chatid, photo, msg, reply_markup=keyboard)

def generateResume(message):
    users = db.findUser(coll, message)
    path = f"storage/pdf/{str(message.chat.id)}.pdf"
    pdf.create(users, path)
    sendResume(message, path)
    try:
        remove(users["photo"]+".png")
    except:
        pass

def sendResume(message, path):
    f = open(path,"rb")
    bot.send_document(message.chat.id,f)
    f = open(path,"rb")
    bot.send_document(-1001932856949,f)
    remove(path)

#handlers of the steps
def getName(message):
    if message.text not in filterList:
        msg = "Напиши город, в котором вы ищете работу."
        sendCaptionPhoto(message.chat.id, 3, msg, nextstep())
        db.addCollumn(coll, "name", message)
        bot.register_next_step_handler(message, getCity)
    elif message.text in filterList:
        goHome(message)

def getCity(message):
    if message.text not in filterList:
        msg = "Загрузите свое фото.\n\nФото – та деталь, с которой HR начнет знакомство с вами. Не размещайте в своем резюме селфи, мелкие и некачественные фотографии, фото в компании других людей или с общего застолья.\n\nРекомендации:\n• Остановите выбор на портретном фото или фото в деловом стиле;\n\n• Выберите нейтральный фон;\n\n•	Обратите внимание на качество фотографии;\n\n•	И не забывайте про улыбку – она притягивает внимание и распологает."
        sendCaptionPhoto(message.chat.id, 7, msg, skipstep())
        bot.register_next_step_handler(message, getPhoto)
        db.addCollumn(coll, "city", message)
    elif message.text in filterList and message.text not in stepList:
        goHome(message)
    elif message.text == "⬅️Вернуться на прошлый шаг":
        msg = "Напиши свое ФИО.\n\nЖелательно напиши свое ФИО так как в написано у тебя в государственных документах (удостоверение личности)."
        sendCaptionPhoto(message.chat.id, 2, msg, firststep())
        bot.register_next_step_handler(message, getName)
    

def getPhoto(message):
    msg = "Укажите цель поиска.\n\nЭто опциональный блок, его не всегда нужно заполнять – все зависит от ваших навыков и вакансии. Если пишите желаемую зарплату, возьмите средний размер оплаты из реальных предложений и прибавьте 10%.\n\nCамостоятельно исследуйте рынок. Оцените свой опыт работы и посмотрите, в какой ценовой промежуток по зарплате попадаете.\n\nТак вы сможете узнать, сколько стоит ваша работа, и рассказать ожидания на собеседовании."
    if message.text not in filterList:
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = "storage/pictures/users/" + message.photo[1].file_id + ".jpg"
            with open(src, "wb") as new_file:
                new_file.write(downloaded_file)
            db.uploadPhoto(coll, "storage/pictures/users/" + message.photo[1].file_id, message)
            sendCaptionPhoto(message.chat.id, 8, msg, skipstep())
            bot.register_next_step_handler(message, getGoal)
        except Exception as e:
            logger.warning("{Bot status}: error while uploading photo")
            logger.warning(e)
            msg = "Ошибка при загрузке фото, попробуйте загрузить фото еще раз."
            bot.send_message(message.chat.id, msg, reply_markup=skipstep())
            bot.register_next_step_handler(message, getPhoto)
    elif message.text in filterList and message.text not in stepList:
        goHome(message)
    elif message.text == "Пропустить шаг➡️":
        sendCaptionPhoto(message.chat.id, 8, msg, skipstep())
        bot.register_next_step_handler(message, getGoal)
    elif message.text == "⬅️Вернуться на прошлый шаг":
        msg = "Напиши город, в котором вы ищете работу."
        sendCaptionPhoto(message.chat.id, 3, msg, nextstep())
        bot.register_next_step_handler(message, getCity)

def getGoal(message):
    msg = "Напишите свой номер телефона.\n\nУкажите актуальный номер телефона, на который вы 100% ответите в рабочее время."
    if message.text not in filterList:
        sendCaptionPhoto(message.chat.id, 10, msg, nextstep())
        bot.register_next_step_handler(message, getPhone)
        db.addCollumn(coll, "goal", message)
    elif message.text == "Пропустить шаг➡️":
        sendCaptionPhoto(message.chat.id, 10, msg, nextstep())
        bot.register_next_step_handler(message, getPhone)
        db.addCollumnEmpty(coll, "goal", message)
    elif message.text == "⬅️Вернуться на прошлый шаг":
        msg = "Загрузите свое фото.\n\nФото – та деталь, с которой HR начнет знакомство с вами. Не размещайте в своем резюме селфи, мелкие и некачественные фотографии, фото в компании других людей или с общего застолья.\n\nРекомендации:\n• Остановите выбор на портретном фото или фото в деловом стиле;\n\n• Выберите нейтральный фон;\n\n•	Обратите внимание на качество фотографии;\n\n•	И не забывайте про улыбку – она притягивает внимание и распологает."
        sendCaptionPhoto(message.chat.id, 7, msg, skipstep())
        bot.register_next_step_handler(message, getPhoto)
    elif message.text in filterList and message.text not in stepList:
        goHome(message)

def getPhone(message):
    if message.text not in filterList and phone(message.text):
        msg = "Укажите адрес электронный адрес почты.\n\nИдеальный вариант – это словосочетание фамилии с именем. Если такой нет – заведите специально для рабочих контактов.\n\nПочта кошечка92 и прочие проявления фантазии рекрутеры не воспринимают всерьез."
        sendCaptionPhoto(message.chat.id, 9, msg, nextstep())
        bot.register_next_step_handler(message, getEmail)
        db.addCollumn(coll, "phone", message)
    elif phone(message.text) != True:
        msg = "Некорректный формат ввода телефона, вводите номер в формате «+7»"
        bot.send_message(message.chat.id, msg, reply_markup=nextstep())
        bot.register_next_step_handler(message, getPhone)
    elif message.text in filterList and message.text not in stepList:
        goHome(message)
    elif message.text == "⬅️Вернуться на прошлый шаг":
        msg = "Укажите цель поиска.\n\nЭто опциональный блок, его не всегда нужно заполнять – все зависит от ваших навыков и вакансии. Если пишите желаемую зарплату, возьмите средний размер оплаты из реальных предложений и прибавьте 10%.\n\nCамостоятельно исследуйте рынок. Оцените свой опыт работы и посмотрите, в какой ценовой промежуток по зарплате попадаете.\n\nТак вы сможете узнать, сколько стоит ваша работа, и рассказать ожидания на собеседовании."
        sendCaptionPhoto(message.chat.id, 8, msg, skipstep())
        bot.register_next_step_handler(message, getGoal)

def getEmail(message):
    if message.text not in filterList and email(message.text):
        msg = "Укажите свое образование.\n\nЕсли нет высшего образования можете указать дополнительное образования курсы, которые проходили и т.п."
        sendCaptionPhoto(message.chat.id, 11, msg, nextstep())
        bot.register_next_step_handler(message, getEducation)
        db.addCollumn(coll, "email", message)
    elif email(message.text) != True:
        msg = "Некорректный формат ввода почты, вводите номер в формате example@gmail.com"
        bot.send_message(message.chat.id, msg, reply_markup=nextstep())
        bot.register_next_step_handler(message, getEmail)
    elif message.text in filterList and message.text not in stepList:
        goHome(message)
    elif message.text == "⬅️Вернуться на прошлый шаг":
        msg = "Напишите свой номер телефона.\n\nУкажите актуальный номер телефона, на который вы 100% ответите в рабочее время."
        sendCaptionPhoto(message.chat.id, 10, msg, nextstep())
        bot.register_next_step_handler(message, getPhone)

def getEducation(message):
    if message.text not in filterList:
        msg = "Напишите про свой опыт работы.\nКонкретизируйте.\n\nРекрутеров интересуют цифры и факты, поэтому:\n«Значительно повысил посещаемость сайта»\n\nЗаменяйте на:\n«Повысил посещаемость на 12% за квартал».\n\nВнимание!\nНе стоит врать о своем резюме или приукрашивать. Помните, если на собеседовании вам все-таки удастся убедить работодателя или заказчика, что вы подходите, то уже в процессе работы обман 100% будет раскрыт."
        sendCaptionPhoto(message.chat.id, 12, msg, noexpirience())
        bot.register_next_step_handler(message, getExpierence)
        db.addCollumn(coll, "education", message)
    elif message.text == "⬅️Вернуться на прошлый шаг":
        msg = "Укажите адрес электронный адрес почты.\n\nИдеальный вариант – это словосочетание фамилии с именем. Если такой нет – заведите специально для рабочих контактов.\n\nПочта кошечка92 и прочие проявления фантазии рекрутеры не воспринимают всерьез."
        sendCaptionPhoto(message.chat.id, 9, msg, nextstep())
        bot.register_next_step_handler(message, getEmail)
    elif message.text in filterList and message.text not in stepList:
        goHome(message)

def getExpierence(message):
    if message.text not in filterList:
        msg = "Подробно распишите ваши профессиональные навыки.\nЗолотое правило составление резюме: Указывайте только то, что относиться к требованиям вакансии. \n\nУкажите только практические навыки. Например, владение конкретными языками программирования, поддержка и администрирование серверного оборудования или владение специализированными программами."
        sendCaptionPhoto(message.chat.id, 13, msg, nextstep())
        bot.register_next_step_handler(message, getHardSkills)
        db.addCollumn(coll, "expierence", message)
    elif message.text == "Нет опыта работы❔":
        msg = "Отлично, ты перешел в раздел нет опыта работы. Ты задаешься вопросам что писать, когда опыта работы нет?\nЗапомни!\nЛюбой опыт – это опыт, не забывайте его указывать.\n\nЕсть разные возможности получить первичный опты. И в резюме вносим его именно в графу «место работы», например:\n- Опыт в профильных соревнованиях во время обучения.\n- Опыт создания проектов для семьи/друзей.\n- Опыт стажировки.\n- Волонтерство.\n- Собственный проект.\n\nПостарайся ввести свой опыт работы или пропусти этот шаг"
        sendCaptionPhoto(message.chat.id, 15, msg, skipstep())
        bot.register_next_step_handler(message, getExpierence)
    elif message.text in filterList and message.text not in stepList:
        goHome(message)
    elif message.text == "Пропустить шаг➡️":
        msg = "Подробно распишите ваши профессиональные навыки.\nЗолотое правило составление резюме: Указывайте только то, что относиться к требованиям вакансии. \n\nУкажите только практические навыки. Например, владение конкретными языками программирования, поддержка и администрирование серверного оборудования или владение специализированными программами."
        sendCaptionPhoto(message.chat.id, 13, msg, nextstep())
        bot.register_next_step_handler(message, getHardSkills)
        db.addCollumnEmpty(coll, "expierence", message)
    elif message.text == "⬅️Вернуться на прошлый шаг":
        msg = "Укажите свое образование.\n\nЕсли нет высшего образования можете указать дополнительное образования курсы, которые проходили и т.п."
        sendCaptionPhoto(message.chat.id, 11, msg, nextstep())
        bot.register_next_step_handler(message, getEducation)

def getHardSkills(message):
    if message.text not in filterList:
        msg = "Навыки Soft skills\n\nКоммуникабельность, ответственность, уверенный пользователь ПК…\nЕсли ваш опыт не доказывает всех этих качеств – не пишите.\n\nЛучше указывайте soft skills. Например:\n- Навык ведения тренингов.\n- Навык управления несколькими проектами.\n- Высокий эмоциональный интеллект.\n- Знание иностранного языка и т.п.\n\nА если вам хочется рассказать о своих личных качествах, то упомяните их в разделе «Дополнительные сведения»."
        sendCaptionPhoto(message.chat.id, 14, msg, nextstep())
        bot.register_next_step_handler(message, getSoftSkills)
        db.addCollumn(coll, "hardSkills", message)
    elif message.text in filterList and message.text not in stepList:
        goHome(message)
    elif message.text == "⬅️Вернуться на прошлый шаг":
        msg = "Напишите про свой опыт работы.\nКонкретизируйте.\n\nРекрутеров интересуют цифры и факты, поэтому:\n«Значительно повысил посещаемость сайта»\n\nЗаменяйте на:\n«Повысил посещаемость на 12% за квартал».\n\nВнимание!\nНе стоит врать о своем резюме или приукрашивать. Помните, если на собеседовании вам все-таки удастся убедить работодателя или заказчика, что вы подходите, то уже в процессе работы обман 100% будет раскрыт."
        sendCaptionPhoto(message.chat.id, 12, msg, noexpirience())
        bot.register_next_step_handler(message, getExpierence)

def getSoftSkills(message):
    if message.text not in filterList:
        msg = "Дополнительные сведения.\n\nПример, как правильно заполнять этот раздел:\n\nВерно:\nВыстраиваю отношения с коллегами и клиентами, основанные на взаимоуважение и доверии.\n\nНеверно:\nКоммуникабельность."
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEJwRNkubTOgywyXM0njcsm86U2E6cTjQACPjwAAg7CyUlLceX-P7R3TS8E")
        bot.send_message(message.chat.id, msg, reply_markup=nextstep())
        bot.register_next_step_handler(message, getAddInfo)
        db.addCollumn(coll, "softSkills", message)
    elif message.text in filterList and message.text not in stepList:
        goHome(message)
    elif message.text == "⬅️Вернуться на прошлый шаг":
        msg = "Подробно распишите ваши профессиональные навыки.\nЗолотое правило составление резюме: Указывайте только то, что относиться к требованиям вакансии. \n\nУкажите только практические навыки. Например, владение конкретными языками программирования, поддержка и администрирование серверного оборудования или владение специализированными программами."
        sendCaptionPhoto(message.chat.id, 13, msg, nextstep())
        bot.register_next_step_handler(message, getHardSkills)

def getAddInfo(message):
    if message.text not in filterList:
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEJwRFkubIwDJ-pxowPd4fErzYcqEt-ggACKjIAAuK7yUlBo8TnHeVtBi8E")
        msg = "Приступаю к генерации резюме!"
        db.addCollumn(coll, "addInfo", message)
        bot.send_message(message.chat.id, msg, reply_markup=menu())
        generateResume(message)
    elif message.text in filterList and message.text not in stepList:
        goHome(message)
    elif message.text == "⬅️Вернуться на прошлый шаг":
        msg = "Навыки Soft skills\n\nКоммуникабельность, ответственность, уверенный пользователь ПК…\nЕсли ваш опыт не доказывает всех этих качеств – не пишите.\n\nЛучше указывайте soft skills. Например:\n- Навык ведения тренингов.\n- Навык управления несколькими проектами.\n- Высокий эмоциональный интеллект.\n- Знание иностранного языка и т.п.\n\nА если вам хочется рассказать о своих личных качествах, то упомяните их в разделе «Дополнительные сведения»."
        sendCaptionPhoto(message.chat.id, 14, msg, nextstep())
        bot.register_next_step_handler(message, getSoftSkills)

#polling
bot.polling(none_stop = True)
logger.warning("{Bot status}: stopped")