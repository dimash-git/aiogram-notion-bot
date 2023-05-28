from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext

from keyboards.inline import create_kb
from states.user_state import UserState
from services.db import update_user, get_user


async def change_leverage(message: types.Message, state: FSMContext):
    try:
        new_leverage = message.text
        user_id = message.from_user.id
        update_user(user_id, {'leverage': int(new_leverage)})

        await message.reply("✅ Leverage update: Success!")
        await state.finish()  # Don't forget to reset the state when you're done
    except Exception as e:
        await message.answer(f'❌ Leverage Update: {str(e)}')


class LeverageCallbacks:
    def __init__(self, bot):
        self.bot = bot

    async def get_leverage_callback(self, callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        user = get_user(user_id)
        if user:
            keyboard = create_kb('⚙️️ Change Leverage', 'change_leverage')
            await self.bot.answer_callback_query(callback_query.id)
            await self.bot.send_message(callback_query.from_user.id,
                                        f"<u>Leverage</u>: {user.get('leverage')}x",
                                        reply_markup=keyboard, parse_mode='HTML')
        else:
            await self.bot.answer_callback_query(callback_query.id, text="User not found in the database.")

    async def change_leverage_callback(self, callback_query: types.CallbackQuery):
        await self.bot.answer_callback_query(callback_query.id)
        await self.bot.send_message(callback_query.from_user.id, 'Please enter the new leverage:')
        await UserState.leverage.set()


def setup(bot: Bot, dp: Dispatcher):
    callbacks = LeverageCallbacks(bot)

    dp.register_message_handler(change_leverage, state=UserState.leverage)

    dp.register_callback_query_handler(callbacks.get_leverage_callback, lambda call: call.data == 'get_leverage')
    dp.register_callback_query_handler(callbacks.change_leverage_callback, lambda call: call.data == 'change_leverage')
