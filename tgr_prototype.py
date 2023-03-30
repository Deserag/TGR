import telebot
from telebot import types

import datetime

import psycopg2

#библиотека для работы с postgresql


# установление соединения с базой данных
conn = psycopg2.connect(dbname='BotDBtest', user='postgres', password='danilworld1', host='127.0.0.1', port='5432')

# создание объекта курсора
cur = conn.cursor()



bot = telebot.TeleBot ("5818591053:AAFZc3LJiRLkzNHIEh4TnBshzHWwIdpSABU")


week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]


group_name = "ИСПк-302-52-00"   #потом будет браться из БД
teacher_name = "Гниенко А.А."   #потом будет браться из БД
day = datetime.datetime.today().weekday()


day_of_week = week[day]          #сегодня
day_tomorrow = week[day+1]       #завтра
#day_tomorrow = "пятница"        #для тестов




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
    
    bot.send_message (message.chat.id, 'Привет, {0.first_name}! Мы рады видеть тебя в числе наших пользователей'.format(message.from_user), reply_markup=markup) #СООБЩЕНИЕ ПРИ НАЖАТИИ СТАРТ

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
            item1 = types.KeyboardButton('Cегодня')
            item2 = types.KeyboardButton('Завтрa')
            item3 = types.KeyboardButton('Tекущая неделя')
            item4 = types.KeyboardButton('Следующая неделя')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, item4 , back)

            bot.send_message (message.chat.id,'🔚Назад',reply_markup=markup)

        elif message.text == 'Сегодня':
            cur.execute(
                "SELECT day, subject, teacher, classroom, lecture_type, lecture_time FROM lecture WHERE group_id ILIKE %s AND day = %s",
                (f"{group_name}%", day_of_week))

            # получение результата и сохранение его в список
            result_list = cur.fetchall()

            # вывод списка
            for row in result_list:
                print(row)

            result_list2 = []
            result_list2 = [row for row in result_list if row[1] is not None or row[2] is not None]

            for row in result_list2:
                print(row)

            text = ""
            for row in result_list2:
                text += f"{row[5]} \n {row[1]} \n {row[4]} \n {row[2]} \n {row[3]}\n"

            print(text)
            text = str(text).replace("None", " ").replace("\n", " ").replace("  ", "")

            print(text)

            bot.send_message(message.chat.id, text)
            text = ""

        elif message.text == 'Завтра':

            cur.execute(
                "SELECT day, subject, teacher, classroom, lecture_type, lecture_time FROM lecture WHERE group_id ILIKE %s AND day = %s",
                (f"{group_name}%", day_tomorrow))

            # получение результата и сохранение его в список
            result_list = cur.fetchall()

            # вывод списка
            for row in result_list:
                print(row)

            result_list2 = []
            result_list2 = [row for row in result_list if row[1] is not None or row[2] is not None]

            for row in result_list2:
                print(row)



            text = ""
            for row in result_list2:
                text += f"{row[5]} \n {row[1]} \n {row[4]} \n {row[2]} \n {row[3]}\n"

            print(text)
            text = str(text).replace("None", " ").replace("\n", " ").replace("  ", "")

            print(text)

            bot.send_message(message.chat.id, text)
            text = ""

        elif message.text == 'Текущая неделя':

            cur.execute(
                "SELECT day, subject, teacher, classroom, lecture_type, lecture_time FROM lecture WHERE group_id = %s",
                (f"{group_name}",))

            result_list = cur.fetchall()

            result_list2 = []
            for row in result_list:
                if all(row[1:]):
                    result_list2.append(row)

            text = ""
            for row in result_list2:
                text +=f"{row[0]} \n {row[5]} \n {row[1]} \n {row[4]} \n {row[2]} \n {row[3]}\n"
            print(text)

            bot.send_message(message.chat.id, text)

        elif message.text == 'Следующая неделя':
            bot.send_message(message.chat.id, 'Вывод расписания на следующую неделю')

        elif message.text == '📳 Вкл.уведомления':
            bot.send_message(message.chat.id, 'Уведомления вкл.')
        
        elif message.text == '📴 Выкл.уведомления':
            bot.send_message(message.chat.id, 'Уведомления выкл.')

# вывод расписания для преподавателей

        elif message.text == 'Cегодня':
            cur.execute(
                "SELECT day, subject, group_id, classroom, lecture_type, lecture_time FROM lecture WHERE teacher ILIKE %s AND day = %s",
                (f"{teacher_name}%", day_of_week))

            # получение результата и сохранение его в список
            result_list = cur.fetchall()

            # вывод списка
            for row in result_list:
                print(row)

            result_list2 = []
            result_list2 = [row for row in result_list if row[1] is not None or row[2] is not None]

            for row in result_list2:
                print(row)

            text = ""
            for row in result_list2:
                text += f"{row[5]} \n {row[1]} \n {row[4]} \n {row[2]} \n {row[3]}\n"

            print(text)
            text = str(text).replace("None", " ").replace("\n", " ").replace("  ", "")

            print(text)

            bot.send_message(message.chat.id, text)
            text = ""


        elif message.text == 'Завтрa':
            cur.execute(
                "SELECT day, subject, group_id, classroom, lecture_type, lecture_time FROM lecture WHERE teacher ILIKE %s AND day = %s",
                (f"{teacher_name}%", day_tomorrow))

            # получение результата и сохранение его в список
            result_list = cur.fetchall()

            # вывод списка
            for row in result_list:
                print(row)

            result_list2 = []
            result_list2 = [row for row in result_list if row[1] is not None or row[2] is not None]

            for row in result_list2:
                print(row)

            text = ""
            for row in result_list2:
                text += f"{row[5]} \n {row[1]} \n {row[4]} \n {row[2]} \n {row[3]}\n"

            print(text)
            text = str(text).replace("None", " ").replace("\n", " ").replace("  ", "")

            print(text)

            bot.send_message(message.chat.id, text)
            text = ""


        elif message.text == 'Tекущая неделя':
            cur.execute(
                "SELECT day, subject, group_id, classroom, lecture_type, lecture_time FROM lecture WHERE teacher = %s",
                (f"{teacher_name}",))

            result_list = cur.fetchall()

            result_list2 = []
            for row in result_list:
                if all(row[1:]):
                    result_list2.append(row)

            text = ""
            for row in result_list2:
                text += f"{row[0]} \n {row[5]} \n {row[1]} \n {row[4]} \n {row[2]} \n {row[3]}\n"
            print(text)

            bot.send_message(message.chat.id, text)

bot.polling(none_stop= True)
