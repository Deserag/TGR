from telebot import TeleBot, types

bot = TeleBot('token')


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text='Привет, как твое имя?')
    bot.register_next_step_handler(message, get_name)

def get_name(message: types.Message):
    print(message.text)
    # тут , то что ввел пользователь
    bot.send_message(chat_id=message.chat.id, text=f'Приятно познакомиться, {message.text}!!!\n'
                                                   f'Напиши свою группу')
    bot.register_next_step_handler(message, get_age)

def get_age(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=f'Твоя группа изменена, {message.text}\n')


bot.polling(skip_pending=True)
