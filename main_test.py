from telegram.ext import Updater, MessageHandler
from telegram.ext import filters


def image_handler(update, context):
    # Получаем объект PhotoSize из сообщения
    photo = update.message.photo[-1]

    # Отправляем изображение пользователю
    context.bot.send_photo(chat_id=update.message.chat_id, photo=photo.file_id)


def main():
    updater = Updater('6056207304:AAE_p4qJMQYAv1mMrXwuZe95naZcbwmd4z8', True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(filters.photo, image_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()