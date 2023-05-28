from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext

from keyboards.inline import create_kb
from states.user_state import UserState
from services.db import update_user, get_user


async def change_size(message: types.Message, state: FSMContext):
    try:
        new_size = message.text
        user_id = message.from_user.id
        update_user(user_id, {'size': {'per_trade': int(new_size)}})

        await message.reply("✅ Size Update: Success!")
        await state.finish()  # Don't forget to reset the state when you're done
    except Exception as e:
        await message.answer(f'❌ Size Update: {str(e)}')


class SizeCallbacks:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def get_size_callback(self, callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        user = get_user(user_id)
        if user:
            keyboard = create_kb('🏦️ Change Size', 'change_size')
            await self.bot.answer_callback_query(callback_query.id)
            await self.bot.send_message(callback_query.from_user.id,
                                        f"<u>Size per trade</u>: {user.get('size', {}).get('per_trade')}$",
                                        reply_markup=keyboard, parse_mode='HTML')
        else:
            await self.bot.answer_callback_query(callback_query.id, text="User not found in the database.")

    async def change_size_callback(self, callback_query: types.CallbackQuery):
        await self.bot.answer_callback_query(callback_query.id)
        await self.bot.send_message(callback_query.from_user.id, 'Please enter the new size per trade:')
        await UserState.size.set()


def setup(bot: Bot, dp: Dispatcher):
    callbacks = SizeCallbacks(bot)

    dp.register_message_handler(change_size, state=UserState.size)

    dp.register_callback_query_handler(callbacks.get_size_callback, lambda call: call.data == 'get_size')
    dp.register_callback_query_handler(callbacks.change_size_callback, lambda call: call.data == 'change_size')
