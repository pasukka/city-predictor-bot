import telebot
from telebot import types
from city_prediction.city_predictor import CityPredictor

cp = CityPredictor()
bot = telebot.TeleBot(cp.key)
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_support = telebot.types.KeyboardButton(text="Сделать заказ")
button_assort = telebot.types.KeyboardButton(text="Узнать ассортимент")
button_info = telebot.types.KeyboardButton(text="Информация о магазине")
keyboard.add(button_support)
keyboard.add(button_assort)
keyboard.add(button_info)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(
        message.chat.id, 'Добро пожаловать в бот заказа цветов! Что бы вы хотели?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_messages(message):
    if message.text == 'Узнать ассортимент':
        assortiment(message)
    elif message.text == 'Информация о магазине':
        information(message)
    elif message.text == 'Сделать заказ':
        bot.send_message(message.chat.id, f'Отлично! Опиши свой заказ!')
        bot.register_next_step_handler(message, get_order_messages)
    else:
        get_order_messages(message)


def information(message):
    text = 'Данный чат-бот создан для некоторого магазина цветов. Он предоставляет анализ текстов сообщения и извлечение из них городов.'
    bot.send_message(message.from_user.id, text)


def assortiment(message):
    list_of_flowers = ['розы', 'хризантемы']
    fl_list = ', '.join(list_of_flowers)
    bot.send_message(message.from_user.id, f'Ассортимент цветов включает следующие позиции: {fl_list}')


def get_order_messages(message):
    city = cp(message.text)
    if city != 'None':
        bot.send_message(message.from_user.id,
                         f'Сейчас переведу Вас на оператора города {city}.')
    else:
        bot.send_message(message.from_user.id,
                         f'Извините, я вас не понимаю. Укажите, пожалуйста, город, в котором вы планируете сделать доставку.')


bot.polling(none_stop=True, interval=0)
