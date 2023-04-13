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


def schedule_weekly():
    cur.execute("SELECT telegram_id, user_group, user_mail FROM users")
    users = cur.fetchall()

    for user in users:
        telegram_id = str(user[0])
        group_name = user[1]
        user_mail = user[2]

        if not user_mail:
            continue  # Если пользователь не хочет получать расписание на почту, то пропускаем его

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
            bot.send_message(telegram_id,
                             'Возникла ошибка при выводе расписания:\nГруппа была занесена в неправильном формате!')
        else:
            bot.send_message(telegram_id, text)
            text = ""


#рассылка расписания
while True:
    now = datetime.datetime.now()
    if now.weekday() == 1 and now.hour == 18: #and now.minute == 29:
        schedule_weekly()
    time.sleep(3)