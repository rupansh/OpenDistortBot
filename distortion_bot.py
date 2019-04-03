from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from io import BytesIO
from glob import glob
import os
from PIL import Image
import random

TOKEN = "ENTER YOUR TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def distort(fname):
    image = Image.open(fname)
    imgdimens = image.width, image.height
    distortcmd = f"magick {fname} -liquid-rescale 60x60%! -resize {imgdimens[0]}x{imgdimens[1]}\! result/{fname}"

    os.system(distortcmd)

    buf = BytesIO()
    buf.name = 'image.jpeg'

    image = Image.open(f"result/{fname}")
    filetype = "JPEG" if fname.endswith(".jpg") else "PNG"
    image.save(buf, filetype)

    buf.seek(0)

    return buf


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("This is a bot based on the distortion bot(@DistortBot). Since its not open source, "
                        "I decided to make an open source verison")


@dp.message_handler(commands=['distort'])
async def dodistort(message):
    for distorted in glob("distorted*"):
        os.remove(distorted)
    for findistorted in glob("*/distorted*"):
        os.remove(findistorted)

    if message.reply_to_message.photo or message.reply_to_message.sticker:
        img = await message.reply_to_message.photo[-1].get_file() if message.reply_to_message.photo \
            else await message.reply_to_message.sticker.get_file()
        imgname = f"distorted{random.randint(1, 100)}"
        imgname += ".jpg" if message.reply_to_message.photo \
            else ".png"

        await img.download(imgname)

        await message.reply_photo(photo=distort(imgname), reply=message)


if __name__ == '__main__':
    executor.start_polling(dp)
