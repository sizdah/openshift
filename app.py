import logging
import requests ,re
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread
from telegram import Bot,ReplyKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters




logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '565668483:AAEgjE0vELcfjk2L05SGLtj0Hc5-XY9unyo' 


def start(bot, update):
    update.message.reply_text('با زدن عبارت phd/ میتونید لیست بورسیه های دکترا رو ببینید')
    update.message.reply_text('با زدن عبارت master/ میتونید لیست بورسیه های فوق لیسانس رو ببینید')
    update.message.reply_text('با زدن عبارت undergraduate/ میتونید لیست بورسیه های لیسانس و قبل از اون رو ببینید')

    bot = Bot(TOKEN)
    id = update.message.from_user.id
    id = int(id)

    custom_keyboard = [
        ['/PhD'],
        ['/Master'],
        ['/Undergraduate']
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=id, text="انتخاب کنید", reply_markup=reply_markup)



def phd(bot, update):

    bot = Bot(TOKEN)
    id = update.message.from_user.id
    id = int(id)

    reply_markup = ReplyKeyboardRemove()
    bot.send_message(chat_id=id, text="آماده سازی", reply_markup=reply_markup)

    try:

        try:
            r = requests.get("https://scholarship-positions.com/category/phd-scholarships-positions")
        except:
            print("can not connect , retry in 60 secs...")


        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        soupo = soup.find_all("h2", {"class": "title entry-title"})



        for item in soupo:

            mes = str(item.text)

            link = item.find_next('a', attrs={'href': re.compile("^https://")})
            print(link.get('href'))
            
            link2 = str(link.get('href'))



            bot.send_message(chat_id=id, text=mes)
            bot.send_message(chat_id=id, text=link2)
            #update.message.reply_text(mes)
            #update.message.reply_text(link)


            # print(item.text)
            # date= jdate.gregorian_to_jd()
    except KeyboardInterrupt:
        print("failed")


def master(bot, update):


    bot = Bot(TOKEN)
    id = update.message.from_user.id
    id = int(id)

    reply_markup = ReplyKeyboardRemove()
    bot.send_message(chat_id=id, text="آماده سازی", reply_markup=reply_markup)


    try:

        try:
            r = requests.get("https://scholarship-positions.com/category/masters-scholarships/")
        except:
            print("can not connect , retry in 60 secs...")

        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        soupo = soup.find_all("h2", {"class": "title entry-title"})



        for item in soupo:
            mes = str(item.text)

            link = item.find_next('a', attrs={'href': re.compile("^https://")})
            print(link.get('href'))

            link2 = str(link.get('href'))


            bot.send_message(chat_id=id, text=mes)
            bot.send_message(chat_id=id, text=link2)
            # update.message.reply_text(mes)
            # update.message.reply_text(link)


            # print(item.text)
            # date= jdate.gregorian_to_jd()
    except KeyboardInterrupt:
        print("failed")



def undergraduate(bot, update):

    bot = Bot(TOKEN)
    id = update.message.from_user.id
    id = int(id)

    reply_markup = ReplyKeyboardRemove()
    bot.send_message(chat_id=id, text="آماده سازی", reply_markup=reply_markup)


    try:

        try:
            r = requests.get("https://scholarship-positions.com/category/under-graduate-scholarship/")
        except:
            print("can not connect , retry in 60 secs...")

        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        soupo = soup.find_all("h2", {"class": "title entry-title"})



        for item in soupo:
            mes = str(item.text)

            link = item.find_next('a', attrs={'href': re.compile("^https://")})
            print(link.get('href'))

            link2 = str(link.get('href'))


            bot.send_message(chat_id=id, text=mes)
            bot.send_message(chat_id=id, text=link2)
            # update.message.reply_text(mes)
            # update.message.reply_text(link)


            # print(item.text)
            # date= jdate.gregorian_to_jd()
    except KeyboardInterrupt:
        print("failed")


def echo(bot, update):
    update.message.reply_text("از دستور راهنمایی استفاده کنید")
    update.message.reply_text("/help")



def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", start))
        dp.add_handler(CommandHandler("phd", phd))
        dp.add_handler(CommandHandler("master", master))
        dp.add_handler(CommandHandler("undergraduate", undergraduate))
        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
