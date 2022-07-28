import logging

from aiogram import Bot, Dispatcher, executor, types


from special_code import GETdefinitions
from googletrans import Translator
translator = Translator()

API_TOKEN = '5577844077:AAFmRVNa18_WOKemsIXsROYstKIy6AjViPQ'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    await message.answer("Hello this is Shohruxs translator bot")


@dp.message_handler(commands=['help'])
async def send_info(message: types.Message):

    await message.answer("You can find any word definition in english with this bot")


@dp.message_handler()
async def tarjimon(message: types.Message):
    lang = translator.detect(message.text).lang
    if len(message.text.split())>2:
        dest = "ru" if lang == "en" else "en"
        await message.reply(translator.translate(message.text, dest).text)
    else:
        if lang == "en":
            word_id = message.text
            lookup = GETdefinitions(word_id)
        else:
            word_id = translator.translate(message.text, dest="en").text
            lookup = GETdefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \n{lookup['definitions']}")
            if lookup.get("audio"):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Bunday soz topilmadi")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)