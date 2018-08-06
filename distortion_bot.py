import telebot
import os
import random

TOKEN = "ENTER_YOUR_TOKEN"
bot = telebot.TeleBot(TOKEN)

user = bot.get_me()

def distort(fname):
    boi = "convert "+fname+" -liquid-rescale 320x320 -implode 0.30 result/"+fname
    os.system(boi)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """Hey! This is a bot based on the distortion bot(@DistortBot). Since its not open source, I decided to make an open
source version. Currently it only supports distorting image and it doesn't have power control (yet).
The source is available at - https://github.com/rupansh/OpenDistortBot""")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Send me an image to distort it! Your photos are deleted after the distortion is complete! To prevent server from hitting its limit, the photo is downscaled to 320x320")


@bot.message_handler(content_types=['photo'])
def photudl(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    download = bot.download_file(file_info.file_path)
    file_name = str(random.randint(1,101))+".jpg"
    with open(file_name, 'wb') as new_file:
        new_file.write(download)
    distort(file_name)
    photo = open('result/'+file_name, 'rb')
    bot.send_photo(message.chat.id, photo)
    os.remove(file_name)
    os.remove("result/"+file_name)


bot.polling()
