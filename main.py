from config import BOT_TOKEN, WEBHOOK_URL

from fastapi import FastAPI, Request
import logging

from aiogram import types
from loader import bot, dp
# from aiogram.utils.exceptions import RetryAfter
# import asyncio


app = FastAPI()
logging.basicConfig(level=logging.DEBUG)


@app.get("/")
def root():
    return {"status": "success", "message": "App started"}


@app.post(f"/{BOT_TOKEN}")
async def handle_update(request: Request):
    if request.method == 'POST':
        try:
            data = await request.json()
            update = types.Update(**data)
            await dp.process_update(update)
            return {'status': 'success', 'message': 'Request received'}
        except Exception as e:
            return {'status': 'error', 'message': f'Error: {e}'}


@app.on_event("startup")
async def startup():
    logging.warning('Starting up..')
    await bot.set_webhook(url=WEBHOOK_URL)
    # Uncomment only if flood control error appears
    # webhook_info = await bot.get_webhook_info()
    #
    # if webhook_info.url != WEBHOOK_URL:
    #     try:
    #         await bot.set_webhook(url=WEBHOOK_URL)
    #     except RetryAfter as e:
    #         await asyncio.sleep(e.timeout)
    #         await bot.set_webhook(url=WEBHOOK_URL)


@app.on_event("shutdown")
async def shutdown():
    logging.warning('Shutting down..')
    await bot.delete_webhook()
