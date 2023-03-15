from aiogram import Bot, Dispatcher, executor, types
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем. 
async def send_welcome(message: types.Message):
   await message.reply("Привет!\nЯ Эхо-бот для работы с расписанием!") 

@dp.message_handler() 
async def echo(message: types.Message): 
    await message.answer(message.text)


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
