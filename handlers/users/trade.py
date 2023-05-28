from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

from states.user_state import UserState
from services.db import get_user, add_trade
from services.notion.notion import create_page
from utils.notion_utils import extract_trade_props


async def on_trade(message: types.Message):
    await message.reply("➡️ Please enter your trade information:")
    await UserState.trade.set()


async def create_trade(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    message_id = message.message_id
    try:
        trade_data = extract_trade_props(message.text)

        if trade_data is None:
            await message.answer("⚠️ Trade information does not satisfy format")
            return

        trade_data['Sum']['number'] = int(get_user(user_id).get('size', {}).get('per_trade'))
        trade_data['Leverage']['number'] = int(get_user(user_id).get('leverage'))

        res = create_page(trade_data)  # notion push

        notion_id = res.json().get('id', '')
        add_trade(user_id, {'notion_id': notion_id, 'message_id': message_id})  # add to mongodb

        if res.status_code != 400:
            await message.reply("✅ Trade has been saved in Notion!")
            await state.finish()  # Don't forget to reset the state when you're done
            return

        await message.answer('❌ Notion: Error creating page')
    except ValueError as e:
        await message.answer(f"⚠️ Regex error: {str(e)}")
    except Exception as e:
        await message.answer(f"❌ An unexpected error occurred: {str(e)}")


def setup(dp: Dispatcher):
    dp.register_message_handler(create_trade, state=UserState.trade)
    dp.register_message_handler(on_trade, commands=['trade'], state='*')
