import telebot
from telebot import types
from random import choice
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps
#from token import *
from parser import *

token = '6056207304:AAE_p4qJMQYAv1mMrXwuZe95naZcbwmd4z8'
bot = telebot.TeleBot(token)
drinks = ['Водка', 'Виски', 'Джин', 'Коньяк', 'Текила', 'Пиво', 'Ничего']
url_github_egor = 'https://github.com/eeroshkin/bot'
url_edadil_winelab = 'https://edadeal.ru/moskva/offers?q=%D0%B2%D0%BE%D0%B4%D0%BA%D0%B0%200%2C5%20%D0%BB&retailer=winelab&sort=aprice'

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
    item3 = types.KeyboardButton('Выведи файлы из реп-я Егора')
    item4 = types.KeyboardButton('Отметь-ка всех')
    item5 = types.KeyboardButton('Отправь фото')
    item6 = types.KeyboardButton('Покажи цены на водку')

    markup_for_group.add(item1, item2, item4, item6)

    markup_for_chat.add(item1, item2, item3, item5, item6)

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


@bot.message_handler(content_types=['text'])
def handle_photo_and_text(message):
    if message.text == "Создатель бота":
        bot.send_message(message.chat.id, "@i_am_monarch")
    elif message.text == "Что выпить":
        bot.send_message(message.chat.id, what_to_drink())
    elif message.text == "Выведи файлы из реп-я Егора":
        bot.send_message(message.chat.id, get_github_data(url_github_egor))
    elif message.text == "Отметь-ка всех":
        bot.send_message(message.chat.id, "@meinatemkalt @i_am_monarch @Sashilo17 @lob_gleb"
                                          " @79161879944 @Dmitriy_Sergeevich_L "
                                          "@79099416254 @Avdey_99 @stocton209r"
                                          " @AsapScarab @VladBernikov ")
        bot.send_message(message.chat.id, "Всех ометил будь здоров!")
    elif message.text == 'Отправь фото':
        photo = open('wallpaper.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
    elif message.text == 'Покажи цены на водку':
        str_AGE_CHECK, str_vodkas = get_vodka_price_winelab(url_edadil_winelab)
        bot.send_message(message.chat.id, f'{str_AGE_CHECK}\nИз ВинЛаба:\n{str_vodkas}')


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.caption == 'Сделай':
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("test_photo.jpg", 'wb') as file:
            file.write(downloaded_file)
        photo_to_change = Image.open("test_photo.jpg")
        changed_photo = ImageOps.grayscale(photo_to_change)

        draw = ImageDraw.Draw(changed_photo)
        font = ImageFont.truetype('Verdana.ttf', 99)
        text = 'Будь здоров'
        color = ImageColor.getrgb("red")

        image_width, image_height = changed_photo.size
        (text_width, text_height, *_)=draw.textbbox((0, 0), text, font=font)
        #text_width, text_height = draw.textsize(text, font)

        center_x = (image_width - text_width) / 14
        center_y = (image_height - text_height) / 2

        draw.text((center_x, center_y), text, font=font, fill="#FF0000")

        bot.send_photo(message.chat.id, changed_photo)



bot.infinity_polling()
