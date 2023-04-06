import telebot
from telebot import types

import datetime
import time
import psycopg2

#библиотека для работы с postgresql


# установление соединения с базой данных
conn = psycopg2.connect(dbname='BotDBtest', user='postgres', password='danilworld1', host='127.0.0.1', port='5432')

# создание объекта курсора
cur = conn.cursor()

#вводим токен бота

bot = telebot.TeleBot ("5818591053:AAFZc3LJiRLkzNHIEh4TnBshzHWwIdpSABU")

#список с днями недели
week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье", "заглушка"]


group_name = "ИСПк-302-52-00"   #потом будет браться из БД
teacher_name = "Гниенко А.А."   #потом будет браться из БД

day = datetime.datetime.today().weekday()   #определение дня недели


day_of_week = week[day]          #сегодня
day_tomorrow = week[day +1]       #завтра


@bot.message_handler(commands = ["start"])

#функция начада работы с ботом
def start (message):
    bot.send_message(message.chat.id, 'Приветсвую тебя пользователь,'
                                      '\n данный бот предназначен для вывода расписания групп коледжа ВятГУ,а также его преподавателей,'
                                      '\n Для дальнейшей работы с ботом введите название своей группы '
                                      '\n Например: ИСПк 302-52-00 '
                                      '\n Если вам нужен преподаватель, то введите его ФИО '
                                      '\n Например: Иванов И.И.')
    # Запрашиваем у пользователя имя его группы
    bot.send_message(message.chat.id, 'Введите имя вашей группы:')
    # Регистрируем обработчик для следующего сообщения пользователя
    bot.register_next_step_handler(message, get_user_group)





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
    #вывод ресурсов вятгу
        elif message.text == 'ℹ Ресурсы ВятГУ':
            spravka = open('resurs.txt', 'r', encoding='utf-8')
            bot.send_message(message.chat.id, spravka.read())
    # создание кнопок рассылки сообщений для админов
        elif message.text == '✉ Рассылка сообщений':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Отправить группе')
            item2 = types.KeyboardButton('🔚Назад')
            item4 = types.KeyboardButton('Отправить всем')
            markup.add(item1, item4, item2)

            bot.send_message(message.chat.id, 'Пожалуйста, выберете кому вы хотите отправить сообщение', reply_markup=markup)
    #выбор получателей
        elif message.text == 'Отправить группе':
            bot.send_message(message.chat.id, 'Введите название группы:')
            bot.register_next_step_handler(message, get_admin_group)
        elif message.text == 'Отправить всем':
            bot.send_message(message.chat.id, 'Введите текст:')
            bot.register_next_step_handler(message, get_admin_text)


    #вывод справки по боту
        elif message.text == '📃 Справка':
            spravka = open('spravka.txt', 'r', encoding='utf-8')
            bot.send_message(message.chat.id, spravka.read())
    #меню настроек
        elif message.text == '⚙ Настройки':
            markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
            item1 = types.KeyboardButton('✏ Изменить групппу')
            item2 = types.KeyboardButton('Вкл.уведомления')
            item3 = types.KeyboardButton('📴 Выкл.уведомления')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, back)

            bot.send_message (message.chat.id,'⚙ Настройки',reply_markup=markup)
    #проверка того является пользователь администратором или нет при выходе в главное меню
        elif message.text == '🔚Назад':

            # Получаем id пользователя
            telegram_id = str(message.from_user.id)

            cur.execute(
                "SELECT user_admin FROM users WHERE telegram_id = %s;",
                (telegram_id,)
            )
            user_admin = cur.fetchone()[0]
            print(user_admin)

            if user_admin:
                markup = types.ReplyKeyboardMarkup(
                    resize_keyboard=True)  # размер кнопок подгоняются зависимо от их количества
                # создание кнопок меню
                item1 = types.KeyboardButton('📚 Расписание')
                item2 = types.KeyboardButton('ℹ Ресурсы ВятГУ')
                item3 = types.KeyboardButton('✉ Рассылка сообщений')
                item4 = types.KeyboardButton('📃 Справка')
                item5 = types.KeyboardButton('⚙ Настройки')
                markup.add(item1, item2, item3, item4, item5)
                bot.send_message(message.chat.id, '🔚Назад', reply_markup=markup)

            else:
                markup = types.ReplyKeyboardMarkup(
                    resize_keyboard=True)  # размер кнопок подгоняются зависимо от их количества
                # создание кнопок меню
                item1 = types.KeyboardButton('📚 Расписание')
                item2 = types.KeyboardButton('ℹ Ресурсы ВятГУ')
                item4 = types.KeyboardButton('📃 Справка')
                item5 = types.KeyboardButton('⚙ Настройки')
                markup.add(item1, item2, item4, item5)
                bot.send_message(message.chat.id, '🔚Назад', reply_markup=markup)

        
        elif message.text == '🔔 Расписание звонков':
            bot.send_message(message.chat.id, 'Вывод расписания звонков')

    #создание кнопок для работы с расписанием
        elif message.text == '🧑‍🎓 Расписание группы':
            markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
            item1 = types.KeyboardButton('Сегодня')
            item2 = types.KeyboardButton('Завтра')
            item3 = types.KeyboardButton('Текущая неделя')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, back)

            bot.send_message (message.chat.id,'🧑‍🎓 Расписание группы',reply_markup=markup)



        elif message.text == '👨‍🏫 Расписание преподавателя':
            bot.send_message(message.chat.id, "Введите имя преподователя:\nВ формате Иванов И.И.")
            bot.register_next_step_handler(message, get_teacher_name)

#вывод расписания для группы

        elif message.text == 'Сегодня':
            #получаем айди пользователя
            telegram_id = str(message.from_user.id)
            #получаем группу пользователя занесённую в бд
            cur.execute("SELECT user_group FROM users WHERE telegram_id = %s", (telegram_id,))
            group_name = cur.fetchone()[0]


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
            if text == "":
                bot.send_message(message.chat.id, 'Возникла ошибка при выводе расписания:\nГруппа была занесена в неправильном формате!')
            else:
                bot.send_message(message.chat.id, text)
                text = ""



        elif message.text == 'Завтра':

            telegram_id = str(message.from_user.id)
            cur.execute("SELECT user_group FROM users WHERE telegram_id = %s", (telegram_id,))
            group_name = cur.fetchone()[0]

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

            if text == "":
                bot.send_message(message.chat.id, 'Возникла ошибка при выводе расписания:\nГруппа была занесена в неправильном формате!')
            else:
                bot.send_message(message.chat.id, text)
                text = ""

        elif message.text == 'Текущая неделя':

            telegram_id = str(message.from_user.id)
            cur.execute("SELECT user_group FROM users WHERE telegram_id = %s", (telegram_id,))
            group_name = cur.fetchone()[0]

            cur.execute(
                "SELECT day, subject, teacher, classroom, lecture_type, lecture_time FROM lecture WHERE group_id = %s",
                (f"{group_name}",))

            result_list = cur.fetchall()
            print(result_list)
            result_list2 = []
            result_list2 = [row for row in result_list if row[1] is not None or row[2] is not None]
            print(result_list2)
            text = ""
            for row in result_list2:
                text += f"{row[0]} \n {row[5]} \n {row[1]} \n {row[4]} \n {row[2]} \n {row[3]}\n"

                new_text = ""
                for line in text.split("\n"):
                    if line.strip():
                        new_text += line + "\n"
            print(new_text)
            text = new_text
            text = str(text).replace("None \n", " ").replace("None", "")
            bot.send_message(message.chat.id, text)


            if text == "":
                bot.send_message(message.chat.id, 'Возникла ошибка при выводе расписания:\nГруппа была занесена в неправильном формате!')
            else:
                bot.send_message(message.chat.id, text)
                text = ""

        elif message.text == 'Вкл.уведомления':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('6:00')
            item2 = types.KeyboardButton('12:00')
            item3 = types.KeyboardButton('Послезавтра')
            item4 = types.KeyboardButton('Текущая неделя')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, item4, back)


        
        elif message.text == '📴 Выкл.уведомления':
            bot.send_message(message.chat.id, 'Уведомления выкл.')

# вывод расписания для преподавателей

        elif message.text == 'Cегодня':
            # получаем айди пользователя
            telegram_id = str(message.from_user.id)
            # получаем преподавателя которого выбрал пользователь
            cur.execute("SELECT user_teacher FROM users WHERE telegram_id = %s", (telegram_id,))

            teacher_name = cur.fetchone()[0]

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

            if text == "":
                bot.send_message(message.chat.id, 'Возникла ошибка при выводе расписания:\nПреподаватель был занесён в неправильном формате/в данный день у преподавателя нет пар')
            else:
                bot.send_message(message.chat.id, text)
                text = ""


        elif message.text == 'Завтрa':

            # получаем айди пользователя
            telegram_id = str(message.from_user.id)
            # получаем преподавателя которого выбрал пользователь
            cur.execute("SELECT user_teacher FROM users WHERE telegram_id = %s", (telegram_id,))

            teacher_name = cur.fetchone()[0]

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

            if text == "":
                bot.send_message(message.chat.id, 'Возникла ошибка при выводе расписания:\nПреподаватель был занесён в неправильном формате/в данный день у преподавателя нет пар')
            else:
                bot.send_message(message.chat.id, text)
                text = ""


        elif message.text == 'Tекущая неделя':

            # получаем айди пользователя
            telegram_id = str(message.from_user.id)
            # получаем преподавателя которого выбрал пользователь
            cur.execute("SELECT user_teacher FROM users WHERE telegram_id = %s", (telegram_id,))

            teacher_name = cur.fetchone()[0]

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

            if text == "":
                bot.send_message(message.chat.id, 'Возникла ошибка при выводе расписания:\nПреподаватель был занесён в неправильном формате/в данный день у преподавателя нет пар')
            else:
                bot.send_message(message.chat.id, text)
                text = ""



        elif message.text == '✏ Изменить групппу':
            # Запрашиваем у пользователя имя его группы
            bot.send_message(message.chat.id, 'Введите имя вашей группы:')
            # Регистрируем обработчик для следующего сообщения пользователя
            bot.register_next_step_handler(message, change_user_group)





#функции (думаю по их названию понятно что они делают)

def get_teacher_name(message):
    # Обновляем переменную teacher_name
    global teacher_name
    teacher_name = message.text
    # Получаем id пользователя
    telegram_id = message.from_user.id
    cur.execute(
        "INSERT INTO users (telegram_id, user_teacher) VALUES (%s, %s) ON CONFLICT (telegram_id) DO UPDATE SET user_teacher = EXCLUDED.user_teacher;",
        (telegram_id, teacher_name)
    )
    conn.commit()

    markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
    item1 = types.KeyboardButton('Cегодня')
    item2 = types.KeyboardButton('Завтрa')
    item3 = types.KeyboardButton('Tекущая неделя')
    back = types.KeyboardButton('🔚Назад')
    markup.add(item1, item2, item3, back)
    bot.send_message (message.chat.id,'👨‍🏫 Расписание преподавателя',reply_markup=markup)

def get_user_group(message):
    # Получаем id пользователя
    telegram_id = str(message.from_user.id)

    cur.execute(
        "SELECT user_admin FROM users WHERE telegram_id = %s;",
        (telegram_id,)
    )
    user_admin = cur.fetchone()[0]
    print(user_admin)
    global user_group
    # Получаем имя группы
    user_group = message.text
    # Записываем данные в таблицу users
    cur.execute(
        "INSERT INTO users (telegram_id, user_group) VALUES (%s, %s) ON CONFLICT (telegram_id) DO UPDATE SET user_group = EXCLUDED.user_group;",
        (telegram_id, user_group)
    )
    conn.commit()

    if user_admin:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # размер кнопок подгоняются зависимо от их количества
        # создание кнопок меню
        item1 = types.KeyboardButton('📚 Расписание')
        item2 = types.KeyboardButton('ℹ Ресурсы ВятГУ')
        item3 = types.KeyboardButton('✉ Рассылка сообщений')
        item4 = types.KeyboardButton('📃 Справка')
        item5 = types.KeyboardButton('⚙ Настройки')
        markup.add(item1, item2, item3, item4, item5)
        bot.send_message(message.chat.id, 'Приятного использования, администратор!', reply_markup=markup)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # размер кнопок подгоняются зависимо от их количества
        # создание кнопок меню
        item1 = types.KeyboardButton('📚 Расписание')
        item2 = types.KeyboardButton('ℹ Ресурсы ВятГУ')
        item4 = types.KeyboardButton('📃 Справка')
        item5 = types.KeyboardButton('⚙ Настройки')
        markup.add(item1, item2, item4, item5)
        bot.send_message(message.chat.id, 'Приятного использования, студент!', reply_markup=markup)

def change_user_group(message):
    # Получаем id пользователя
    telegram_id = message.from_user.id
    global user_group
    # Получаем имя группы
    user_group = message.text
    # Записываем данные в таблицу users
    cur.execute(
        "INSERT INTO users (telegram_id, user_group) VALUES (%s, %s) ON CONFLICT (telegram_id) DO UPDATE SET user_group = EXCLUDED.user_group;",
        (telegram_id, user_group)
    )
    conn.commit()
    #заново делаем кнопочки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('✏ Изменить групппу')
    item2 = types.KeyboardButton('📳 Вкл.уведомления')
    item3 = types.KeyboardButton('📴 Выкл.уведомления')
    back = types.KeyboardButton('🔚Назад')
    markup.add(item1, item2, item3, back)
    bot.send_message(message.chat.id, 'Группа успешно изменена')



def get_admin_group(message):
    global admin_group
    admin_group = message.text
    bot.send_message(message.chat.id, 'Введите текст сообщения:')
    bot.register_next_step_handler(message, send_message_to_group)


def send_message_to_group(message):
    admin_text = message.text
    admin_id = message.chat.id
    cur.execute("SELECT telegram_id FROM users WHERE user_group = %s", (admin_group,))
    rows = cur.fetchall()


    for row in rows:
        bot.send_message(row[0], 'НОВОЕ СООБЩЕНИЕ ОТ АДМИНИСТРАЦИИ:\n{}'.format(admin_text))
    cur.execute(
        "INSERT INTO history_message (sender_message, text_message, group_message) VALUES (%s, %s, %s)",
        (admin_id, admin_text, admin_group)
    )
    conn.commit()


def get_admin_text(message):
    admin_text = message.text
    admin_id = message.chat.id
    cur.execute("SELECT telegram_id FROM users")
    rows = cur.fetchall()
    for row in rows:
        bot.send_message(row[0], 'НОВОЕ СООБЩЕНИЕ ОТ АДМИНИСТРАЦИИ:\n{}'.format(admin_text))
    cur.execute(
        "INSERT INTO history_message (sender_message, text_message) VALUES (%s, %s)",
        (admin_id, admin_text)
    )
    conn.commit()






bot.polling(none_stop= True)
