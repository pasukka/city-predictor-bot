import telebot
from city_prediction.city_predictor import CityPredictor

cp = CityPredictor()
bot = telebot.TeleBot(cp.key)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(f'Message: {message.text}')
    city = cp(message.text)
    print(f'City: {city}')
    bot.send_message(message.from_user.id, f'Да, конечно, мы можем доставить в {city}')

bot.polling(none_stop=True, interval=0)


# city = cp("доставка в питер есть?")
# print(f'City: {city}')

