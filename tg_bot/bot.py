import config
import logging

from aiogram import Bot, Dispatcher, executor, types
from filters import IsAdminFilter

# log lvl
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# activate filters
dp.filters_factory.bind(IsAdminFilter)

# ban command (admins only)
@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix='!/')
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта комманда должна быть ответом на сообщение")
        return
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user_id)

    await message.reply_to_message.reply("Пользователь забанен!\nПравосудие свершилось")


# remove new user joined messages
@dp.message_handler(content_types['new_chat_members'])
async def on_uswe_joined(message: types.Message):
    await message.delete()


# delete bad words
@dp.message_handker()
async def filter_messages(message: types.Message):
    if "плохие слова" in message.text:
        await message.delete()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
