import telebot
from telebot import types

bot = telebot.TeleBot('6250495165:AAFPkRdtt8OMpEjHc-3n50afVH6ytQ1H6VI')
#
@bot.message_handler(commands=['schedule'])
def schedule(message):
    markup_inline = types.InlineKeyboardMarkup()
    rasp_prepod = types.InlineKeyboardButton(text= 'Преподавателя', callback_data= 'rasp_prepod')
    rasp_group = types.InlineKeyboardButton(text= 'Группы', callback_data='rasp_group')

    markup_inline.add(rasp_prepod, rasp_group)
    bot.send_message(message.chat.id, 'Выберите расписание', reply_markup= markup_inline)

@bot.callback_query_handler(func= lambda call: True)
def schedule(call):
    if call.data == 'Расписание преподавателя':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard= True)
        today = types.KeyboardButton('Сегодня')
        tomorrow = types.KeyboardButton('Завтра')
        next_week = types.KeyboardButton('Следующая неделя')
        last_week = types.KeyboardButton('Предыдущая неделя')

        markup_reply.add(today, tomorrow, next_week, last_week)
        bot.send_message(call.message.chat.id, 'Нажмите на одну из кнопок', reply_markup= markup_reply)

    elif call.data == 'Расписание группы':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        today = types.KeyboardButton('Сегодня')
        tomorrow = types.KeyboardButton('Завтра')
        next_week = types.KeyboardButton('Следующая неделя')
        last_week = types.KeyboardButton('Предыдущая неделя')
        markup_reply.add(today, tomorrow, next_week, last_week)

        bot.send_message(call.message.chat.id, 'Нажмите на одну из кнопок', reply_markup= markup_reply)

@bot.message_handler(content_types=['text'])
def content(message):
        if message.text == 'Сегодня':
            bot.send_message(message.chat.id, f'fРасписание на сегодня{message.from_user.first_name} {message.from_user.last_name}:')
        elif message.text == 'Завтра':
            bot.send_message(message.chat.id, f'fРасписание на завтра{message.from_user.first_name} {message.from_user.last_name}:')
        elif message.text == 'Следующая неделя':
            bot.send_message(message.chat.id, f'fРасписание на следующую неделю{message.from_user.first_name} {message.from_user.last_name}:')
        elif message.text == 'Предыдущая неделя':
            bot.send_message(message.chat.id, f'fРасписание на предыдущую неделю{message.from_user.first_name} {message.from_user.last_name}:')


bot.polling(none_stop= True)
