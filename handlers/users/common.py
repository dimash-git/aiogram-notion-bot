from aiogram import types
from aiogram import Dispatcher

from keyboards.inline import create_kb_multi
from services.db import get_trade, get_user, update_user
from services.notion.notion import update_page
from utils.notion_utils import attach_trade_props


async def on_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    user = get_user(user_id)

    if user is None:
        user_data = {
            "size": {
                "per_trade": 100
            },
            "trades": [],
            "leverage": 1
        }
        update_user(user_id, user_data)
        await message.reply("➡️ Your user profile was created successfully!")
        return
    await message.reply(f"Hello {username} 👋")


async def on_info(message: types.Message):
    buttons = [
        ('🏦️ My Size', 'get_size'),
        ('⚙️ My Leverage', 'get_leverage')
    ]
    keyboard = create_kb_multi(buttons)
    await message.reply("➡️ What would you like to do next?", reply_markup=keyboard)


async def on_reply(message: types.Message):
    if message.reply_to_message is not None:
        og_message_id = message.reply_to_message.message_id
        user_id = message.from_user.id
        try:
            trade = get_trade(user_id, og_message_id)

            trade_data = attach_trade_props(message.text)
            notion_page_id = trade['notion_id']
            update_page(trade_data, notion_page_id)

            await message.answer(f"✅ Trade Update: Success!")
        except Exception as e:
            await message.answer(f"❌ Trade Update: {str(e)}")
    else:
        await message.answer("This message is not a reply.")


def setup(dp: Dispatcher):
    dp.register_message_handler(on_start, commands=['start'], state='*')
    dp.register_message_handler(on_info, commands=['profile'], state='*')
    dp.register_message_handler(on_reply)
