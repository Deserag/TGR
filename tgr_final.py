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

admin_tags = []
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
                                      '\n Например: ИСПк-302-52-00 '
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

            text = '''
            <b>Ресурсы ВятГУ:</b>

            <a href="https://www.vyatsu.ru/">Сайт ВятГУ</a>

            <a href="https://new.vyatsu.ru/account/">Личный кабинет</a>

            <a href="https://e.vyatsu.ru/">Электронные учебные курсы (мудл)</a>

            <a href="https://lib.vyatsu.ru/?LNG=&C21COM=F&I21DBN=IBIS&P21DBN=IBIS">Электронная библиотека</a>

            <a href="https://vk.com/kollegevyatsu">Группа ВК колледжа</a>
            '''

            bot.send_message(message.chat.id, text=text, parse_mode='HTML')


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
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('тег1')
            item2 = types.KeyboardButton('тег2')
            item3 = types.KeyboardButton('тег3')
            item4 = types.KeyboardButton('Продолжить')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, item4, back)
            bot.send_message(message.chat.id, 'Выберите теги:', reply_markup=markup)
            bot.register_next_step_handler(message, get_tags_to_all)


    #вывод справки по боту
        elif message.text == '📃 Справка':
            spravka = open('spravka.txt', 'r', encoding='utf-8')
            bot.send_message(message.chat.id, spravka.read())
    #меню настроек
        elif message.text == '⚙ Настройки':
            markup = types.ReplyKeyboardMarkup (resize_keyboard= True)
            item1 = types.KeyboardButton('✏ Изменить групппу')
            item2 = types.KeyboardButton('📳 Вкл.уведомления')
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


        elif message.text == '📳 Вкл.уведомления':
            # Получаем id пользователя
            telegram_id = message.from_user.id
            # Записываем данные в таблицу users
            cur.execute(
                "INSERT INTO users (telegram_id, user_mail) VALUES (%s, %s) ON CONFLICT (telegram_id) DO UPDATE SET user_mail = TRUE;",
                (telegram_id, True)
            )

            conn.commit()
            # заново делаем кнопочки
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('✏ Изменить групппу')
            item2 = types.KeyboardButton('📳 Вкл.уведомления')
            item3 = types.KeyboardButton('📴 Выкл.уведомления')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, back)
            bot.send_message(message.chat.id, 'Рассылка расписания успешно включена')


        elif message.text == '📴 Выкл.уведомления':
            # Получаем id пользователя
            telegram_id = message.from_user.id
            # Записываем данные в таблицу users
            cur.execute(
                "INSERT INTO users (telegram_id, user_mail) VALUES (%s, %s) ON CONFLICT (telegram_id) DO UPDATE SET user_mail = FALSE;",
                (telegram_id, False)
            )

            conn.commit()
            # заново делаем кнопочки
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('✏ Изменить групппу')
            item2 = types.KeyboardButton('📳 Вкл.уведомления')
            item3 = types.KeyboardButton('📴 Выкл.уведомления')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, back)
            bot.send_message(message.chat.id, 'Рассылка расписания успешно выключена')



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



            result_list2 = []
            result_list2 = [row for row in result_list if row[1] is not None or row[2] is not None]


            text = ""


            current_day = ""
            for lesson in result_list2:
                if lesson[0] != current_day:
                    current_day = lesson[0]
                    text += f"\n——{current_day}——\n\n"
                text += f"——/ {lesson[5]} /——\n{lesson[1]}\n{lesson[4]}\n{lesson[2]}\n{lesson[3]}\n\n"



            text = str(text).replace("None \n", " ").replace("None", "")


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



            result_list2 = []
            result_list2 = [row for row in result_list if row[1] is not None or row[2] is not None]





            text = ""


            current_day = ""
            for lesson in result_list2:
                if lesson[0] != current_day:
                    current_day = lesson[0]
                    text += f"\n——{current_day}——\n\n"
                text += f"——/ {lesson[5]} /——\n{lesson[1]}\n{lesson[4]}\n{lesson[2]}\n{lesson[3]}\n\n"


            text = str(text).replace("None \n", " ").replace("None", "")



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

            result_list2 = []
            result_list2 = [row for row in result_list if row[1] is not None or row[2] is not None]


            text = ""
            current_day = ""
            for lesson in result_list2:
                if lesson[0] != current_day:
                    current_day = lesson[0]
                    text += f"\n——{current_day}——\n\n"
                text += f"——/ {lesson[5]} /——\n{lesson[1]}\n{lesson[4]}\n{lesson[2]}\n{lesson[3]}\n\n"

            text = str(text).replace("None \n", " ").replace("None", "")


            if text == "":
                bot.send_message(message.chat.id, 'Возникла ошибка при выводе расписания:\nГруппа была занесена в неправильном формате!')
            else:
                bot.send_message(message.chat.id, text)
                text = ""

        elif message.text == '📳 Вкл.уведомления':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('6:00')
            item2 = types.KeyboardButton('12:00')
            item3 = types.KeyboardButton('Послезавтра')
            item4 = types.KeyboardButton('Текущая неделя')
            back = types.KeyboardButton('🔚Назад')
            markup.add(item1, item2, item3, item4, back)


        


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


            result_list2 = []
            result_list2 = [row for row in result_list if row[1] is not None or row[2] is not None]


            text = ""
            current_day = ""
            for lesson in result_list2:
                if lesson[0] != current_day:
                    current_day = lesson[0]
                    text += f"\n——{current_day}——\n\n"
                text += f"——/ {lesson[5]} /——\n{lesson[1]}\n{lesson[4]}\n{lesson[2]}\n{lesson[3]}\n\n"





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



            result_list2 = []
            result_list2 = [row for row in result_list if row[1] is not None or row[2] is not None]


            text = ""
            current_day = ""
            for lesson in result_list2:
                if lesson[0] != current_day:
                    current_day = lesson[0]
                    text += f"\n——{current_day}——\n\n"
                text += f"——/ {lesson[5]} /——\n{lesson[1]}\n{lesson[4]}\n{lesson[2]}\n{lesson[3]}\n\n"



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



            days_of_week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

            sorted_list = sorted(result_list2, key=lambda x: days_of_week.index(x[0]))

            text = ""
            current_day = ""
            for lesson in sorted_list:
                if lesson[0] != current_day:
                    current_day = lesson[0]
                    text += f"\n——{current_day}——\n\n"
                text += f"——/ {lesson[5]} /——\n{lesson[1]}\n{lesson[4]}\n{lesson[2]}\n{lesson[3]}\n\n"



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






#получаем преподавателя и закрепляем за пользователем в бд

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

#функция получения группы пользователя при начале работы с ботом и проверка на администратора

def get_user_group(message):
    telegram_id = str(message.from_user.id)
    global user_group
    # Получаем имя группы
    user_group = message.text
    # Записываем данные в таблицу users
    cur.execute(
        "INSERT INTO users (telegram_id, user_group) VALUES (%s, %s) ON CONFLICT (telegram_id) DO UPDATE SET user_group = EXCLUDED.user_group;",
        (telegram_id, user_group)
    )
    conn.commit()

    # Получаем id пользователя
    telegram_id = str(message.from_user.id)

    cur.execute(
        "SELECT user_admin FROM users WHERE telegram_id = %s;",
        (telegram_id,)
    )
    user_admin = str(cur.fetchone()[0])




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

#функция смены группы пользователя в бд

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


#функция получения группы для рассылки сообщения администратором и переход к следующему шагу

def get_admin_group(message):
    global admin_group
    admin_group = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('тег1')
    item2 = types.KeyboardButton('тег2')
    item3 = types.KeyboardButton('тег3')
    item4 = types.KeyboardButton('Продолжить')
    back = types.KeyboardButton('🔚Назад')
    markup.add(item1, item2, item3, item4, back)
    bot.send_message(message.chat.id, 'Выберите теги:', reply_markup=markup)
    bot.register_next_step_handler(message, get_tags)


#функция отправки сообщения от администрации всем пользователям в группе

def send_message_to_group(message):
    admin_text = message.text
    admin_id = message.chat.id



    cur.execute(
        "INSERT INTO history_message (sender_message, text_message, group_message) VALUES (%s, %s, %s)",
        (admin_id, admin_text, admin_group)
    )
    conn.commit()

    cur.execute("SELECT telegram_id FROM users WHERE user_group = %s", (admin_group,))
    rows = cur.fetchall()
    global admin_tags
    # объединяем теги в строку
    tags_str = ' '.join(['#' + tag for tag in admin_tags])

    full_message = f'{tags_str} \n \n {admin_text}'


    for row in rows:
        bot.send_message(row[0], 'НОВОЕ СООБЩЕНИЕ ОТ АДМИНИСТРАЦИИ:\n{}'.format(full_message))

    admin_tags.clear()


#функция отправки сообщений от администрации всем пользователям

def get_admin_text(message):
    admin_text = message.text
    admin_id = message.chat.id

    cur.execute(
        "INSERT INTO history_message (sender_message, text_message, group_message) VALUES (%s, %s)",
        (admin_id, admin_text)
    )
    conn.commit()

    cur.execute("SELECT telegram_id FROM users")
    rows = cur.fetchall()
    global admin_tags
    # объединяем теги в строку
    tags_str = ' '.join(['#' + tag for tag in admin_tags])

    full_message = f'{tags_str} \n \n {admin_text}'

    for row in rows:
        bot.send_message(row[0], 'НОВОЕ СООБЩЕНИЕ ОТ АДМИНИСТРАЦИИ:\n{}'.format(full_message))

    admin_tags.clear()


#функция для выбора нужных администратору тегов

def get_tags(message):
    global admin_tags
    if message.text == 'тег1' or message.text == 'тег2' or message.text == 'тег3':
        admin_tags.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('тег1')
        item2 = types.KeyboardButton('тег2')
        item3 = types.KeyboardButton('тег3')
        item4 = types.KeyboardButton('Продолжить')
        back = types.KeyboardButton('🔚Назад')
        markup.add(item1, item2, item3, item4, back)
        bot.send_message(message.chat.id, 'Выберите теги:', reply_markup=markup)
        bot.register_next_step_handler(message, get_tags)
    elif message.text == 'Продолжить':

        bot.send_message(message.chat.id, 'Введите текст сообщения:')
        bot.register_next_step_handler(message, send_message_to_group)


def get_tags_to_all(message):
    global admin_tags
    if message.text == 'тег1' or message.text == 'тег2' or message.text == 'тег3':
        admin_tags.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('тег1')
        item2 = types.KeyboardButton('тег2')
        item3 = types.KeyboardButton('тег3')
        item4 = types.KeyboardButton('Продолжить')
        back = types.KeyboardButton('🔚Назад')
        markup.add(item1, item2, item3, item4, back)
        bot.send_message(message.chat.id, 'Выберите теги:', reply_markup=markup)
        bot.register_next_step_handler(message, get_tags)
    elif message.text == 'Продолжить':

        bot.send_message(message.chat.id, 'Введите текст сообщения:')
        bot.register_next_step_handler(message, get_admin_text)


bot.polling(none_stop= True)
