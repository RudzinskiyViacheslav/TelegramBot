import telebot
from telebot import types
from random import choice
from PIL import Image
from token import *

bot = telebot.TeleBot(token)
drinks = ['Водка','Виски','Джин','Коньяк','Текила','Пиво','Ничего']

def what_to_drink():
    drink = choice(drinks)
    return drink


# @bot.message_handler(commands=['start'], content_types=['text', 'audio'])


# @bot.message_handler(commands=['button'])
# def button_message(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton('Создатель бота')
#     item2 = types.KeyboardButton('Что выпить')
#     item3 = types.KeyboardButton('Лесенка')
#     markup.add(item1, item2, item3)
#     bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(commands=['start'])
def start_message(message):

    markup_for_group = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup_for_chat = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Создатель бота')
    item2 = types.KeyboardButton('Что выпить')
    item3 = types.KeyboardButton('Лесенка')
    item4 = types.KeyboardButton('Отметь-ка всех')
    item5 = types.KeyboardButton('Отправь фото')

    markup_for_group.add(item1, item2, item3, item4)

    markup_for_chat.add(item1, item2, item3, item5)

    if message.chat.type == 'private':
        bot.send_message(message.chat.id, f'Приветик {message.from_user.username}', reply_markup=markup_for_chat)
    elif message.chat.type == 'group' or message.chat.type == 'supergroup':
        bot.send_message(message.chat.id, f'Приветик {message.from_user.username}', reply_markup=markup_for_group)
    # print(f"{message.from_user.username} пишет {message.text}")
    # if message.text == "Привет":
    # print(f"{message.from_user.username} пишет {message.text}")
    # bot.send_message(message.from_user.id, f"Ну здравствуй! {message.from_user.username}")
    # else:
    # bot.send_message(message.from_user.id, "Славик фигачит бота. Напиши что-нибудь нормальное")


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Создатель бота":
        bot.send_message(message.chat.id, "@i_am_monarch")
    elif message.text == "Что выпить":
        bot.send_message(message.chat.id, what_to_drink())
    elif message.text == "Лесенка":
        bot.send_message(message.chat.id, "1-я ступеня - лох, 2-я - Коля"
                                          " ... 7-я - Авдей")
    elif message.text == "Отметь-ка всех":
        bot.send_message(message.chat.id, "@meinatemkalt @i_am_monarch @Sashilo17 @lob_gleb"
                                          " @79161879944 @Dmitriy_Sergeevich_L "
                                          "@79099416254 @Avdey_99 @stocton209r"
                                          " @AsapScarab @VladBernikov ")
        bot.send_message(message.chat.id, "Всех ометил будь здоров!")
    elif message.text == 'Отправь фото':
        photo = open('wallpaper.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("test_photo.jpg", 'wb') as file:
        file.write(downloaded_file)
    photo_to_change = Image.open("test_photo.jpg")
    changed_photo = photo_to_change.convert("L")

    bot.send_photo(message.chat.id, changed_photo)

bot.polling()




bot.infinity_polling()
