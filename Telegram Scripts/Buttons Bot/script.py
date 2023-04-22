import os
import asyncio
import telegram
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PUBLIC_CHANNEL = os.getenv("PUBLIC_CHANNEL")
PRIVATE_CHANNEL = os.getenv("PRIVATE_CHANNEL")
BIN_CHANNEL = os.getenv("BIN_CHANNEL")

bot = telegram.Bot(token=BOT_TOKEN)

image_url = 'https://m.economictimes.com/thumb/msid-97434971,width-1280,height-720,resizemode-4,imgsize-183376/pathaan.jpg'
keyboard = [[InlineKeyboardButton("480p", url='www.github.com/pyguru123'),
             InlineKeyboardButton("720p", url='www.github.com/pyguru123')]]
reply_markup = InlineKeyboardMarkup(keyboard)

chat_ids = [PUBLIC_CHANNEL, PRIVATE_CHANNEL, BIN_CHANNEL]
async def send_photo():
	for _id in chat_ids:
		await bot.send_photo(chat_id=_id, photo=image_url, caption='This is the caption', reply_markup=reply_markup)

async def main():
    await send_photo()

# Or use asyncio.run() to run the event loop
if __name__ == '__main__':
    asyncio.run(send_photo())