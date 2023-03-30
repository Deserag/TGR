import telebot
from telebot import types

bot = telebot.TeleBot ("")

@bot.message_handler(commands = ["start"])
def start (message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup (resize_keyboard= True) 
    item1 = types.KeyboardButton('📚 Расписание')
    item2 = types.KeyboardButton('ℹ Ресурсы ВятГУ')
    item3 = types.KeyboardButton('✉ Уведомления от администрации')
    item4 = types.KeyboardButton('📃 Справка')
    item5 = types.KeyboardButton('⚙ Настройки')
    markup.add(item1, item2, item3, item4, item5)
    
    bot.send_message (message.chat.id, 'Привет, {0.first_name}!Мы рады видеть тебя в числе наших пользователей'.format(message.from_user), reply_markup=markup) #СООБЩЕНИЕ ПРИ НАЖАТИИ СТАРТ

@bot.message_handler(content_types=['text'])
def bot_message(message):
    user_id = message.from_user.id
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

        elif message.text == '✉ Уведомления от администрации':
            markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
            item1 = types.KeyboardButton('Написать сообщение')
            item2 = types.KeyboardButton('Выбрать получателя')
            item3 = types.KeyboardButton('Отправить')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, back)

            bot.send_message (message.chat.id,'✉ Уведомления от администрации',reply_markup=markup)
                #bot.send_message(message.chat.id, 'Вывод уведомлений от администрации')  
                  
        elif message.text == 'Выбрать получателя':
            markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
            item1 = types.KeyboardButton('Всем')
            item2 = types.KeyboardButton('Группа')
            item3 = types.KeyboardButton('Поток')
            item4 = types.KeyboardButton('Курс')
            back2 = types.KeyboardButton('Назад')
            markup.add(item1, item2, item3, item4 , back2)

            bot.send_message (message.chat.id,'Выбрать получателя',reply_markup=markup)

        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
            item1 = types.KeyboardButton('Написать сообщение')
            item2 = types.KeyboardButton('Выбрать получателя')
            item3 = types.KeyboardButton('Отправить')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, back)

            bot.send_message (message.chat.id,'Назад',reply_markup=markup)
        
        elif message.text == 'Написать сообщение':
            bot.send_message(message.chat.id, 'Админ вводит текст уведомления')

        elif message.text == 'Всем':
            bot.send_message(message.chat.id, 'Рассылка уведомления всем студентам')

        elif message.text == 'Группа':
            bot.send_message(message.chat.id, 'Рассылка уведомления введенной группе')

        elif message.text == 'Поток':
            bot.send_message(message.chat.id, 'Рассылка уведомления выбранному потоку')

        elif message.text == 'Курс':
            bot.send_message(message.chat.id, 'Рассылка уведомления выбранному курсу')

    
        elif message.text == 'Отправить':
            bot.send_message(message.chat.id, 'Сообщение отправлено')

bot.polling(none_stop= True)
