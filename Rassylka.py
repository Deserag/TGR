import telebot

bot = telebot.TeleBot('6250495165:AAFPkRdtt8OMpEjHc-3n50afVH6ytQ1H6VI')

#Создаем текстовый файл для записи id пользователя
@bot.message_handler(commands=['start'])
def start(message):
    with open('chatids.txt', 'a+') as chatids:
        print(message.chat.id, file=chatids)

#Делаем проверку пользователя на администратора
@bot.message_handler(commands=['rassylka'])
def rassylka(message):
    if message.chat.id == 5230826045:
        for i in open('chatids.txt', 'r').readlines():
            bot.send_message(i, 'Рассылка расписания')

bot.polling(none_stop=True)