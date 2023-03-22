import telebot
from telebot import types

bot = telebot.TeleBot ()

@bot.message_handler(commands = ["start"])
def start (message):

    markup = types.ReplyKeyboardMarkup (resize_keyboard= True) #размер кнопок подгоняются зависимо от их количества
    #создание кнопок меню
    item1 = types.KeyboardButton('📚 Расписание')
    item2 = types.KeyboardButton('ℹ Ресурсы ВятГУ')
    item3 = types.KeyboardButton('✉ Уведомления от администрации')
    item4 = types.KeyboardButton('📃 Справка')
    item5 = types.KeyboardButton('⚙ Настройки')
    markup.add(item1, item2, item3, item4, item5)
    
    bot.send_message (message.chat.id, 'Привет, {0.first_name}!Мы рады видеть тебя в числе наших пользователей'.format(message.from_user), reply_markup=markup) #СООБЩЕНИЕ ПРИ НАЖАТИИ СТАРТ

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '📚 Расписание':
            markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
            item1 = types.KeyboardButton('🧑‍🎓 Расписание группы')
            item2 = types.KeyboardButton('👨‍🏫 Расписание преподавателя')
            item3 = types.KeyboardButton('🔔 Расписание звонков')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, back)

            bot.send_message (message.chat.id,'📚 Расписание',reply_markup=markup)
        elif message.text == 'ℹ Ресурсы ВятГУ':
            bot.send_message(message.chat.id, 'Здесь ссылки на ресурсы')

        elif message.text == '✉ Уведомления от администрации':
            bot.send_message(message.chat.id, 'Вывод уведомлений от администрации')

        elif message.text == '📃 Справка':
            bot.send_message(message.chat.id, 'Вывод справки')

        elif message.text == '⚙ Настройки':
            markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
            item1 = types.KeyboardButton('✏ Изменить групппу')
            item2 = types.KeyboardButton('📳 Вкл.уведомления')
            item3 = types.KeyboardButton('📴 Выкл.уведомления')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, back)

            bot.send_message (message.chat.id,'⚙ Настройки',reply_markup=markup)

        elif message.text == '🔚Назад':
            markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
            item1 = types.KeyboardButton('📚 Расписание')
            item2 = types.KeyboardButton('ℹ Ресурсы ВятГУ')
            item3 = types.KeyboardButton('✉ Уведомления от администрации')
            item4 = types.KeyboardButton('📃 Справка')
            item5 = types.KeyboardButton('⚙ Настройки')
            markup.add(item1, item2, item3, item4, item5)

            bot.send_message (message.chat.id,'🔚Назад',reply_markup=markup)
        
        elif message.text == '🔔 Расписание звонков':
            bot.send_message(message.chat.id, 'Вывод расписания звонков')


        elif message.text == '🧑‍🎓 Расписание группы':
            markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
            item1 = types.KeyboardButton('Сегодня')
            item2 = types.KeyboardButton('Завтра')
            item3 = types.KeyboardButton('Текущая неделя')
            item4 = types.KeyboardButton('Следующая неделя')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, item4 , back)

            bot.send_message (message.chat.id,'🧑‍🎓 Расписание группы',reply_markup=markup)


        elif message.text == '👨‍🏫 Расписание преподавателя':
            markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
            item1 = types.KeyboardButton('Сегодня')
            item2 = types.KeyboardButton('Завтра')
            item3 = types.KeyboardButton('Текущая неделя')
            item4 = types.KeyboardButton('Следующая неделя')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, item4 , back)

            bot.send_message (message.chat.id,'🔚Назад',reply_markup=markup)

        elif message.text == 'Сегодня':
            bot.send_message(message.chat.id, 'Вывод расписания на сегодняшний день')

        elif message.text == 'Завтра':
            bot.send_message(message.chat.id, 'Вывод расписания на завтрашний день')

        elif message.text == 'Текущая неделя':
            bot.send_message(message.chat.id, 'Вывод расписания на текущую неделю')

        elif message.text == 'Следующая неделя':
            bot.send_message(message.chat.id, 'Вывод расписания на следующую неделю')

        elif message.text == '📳 Вкл.уведомления':
            bot.send_message(message.chat.id, 'Уведомления вкл.')
        
        elif message.text == '📴 Выкл.уведомления':
            bot.send_message(message.chat.id, 'Уведомления выкл.')
               

bot.polling(none_stop= True)
