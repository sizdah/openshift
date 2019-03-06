import logging
from queue import Queue
from threading import Thread
from telegram import Bot,ReplyKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters
import re,glob,os

import feedparser
from googletrans import Translator


lock = False
query_mem = ""

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '691443857:AAHX-40RGGdBG-2d_aAZyFKdSbQ0VcYvTHc'





def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def get(bot, update):
    menza = "https://jidelnicek.utb.cz/WebKredit/rss?canteenId=3&language=En"

    d = feedparser.parse(menza)
    data = cleanhtml(d.entries[1]["summary"])


    translator = Translator()

    en_data = translator.translate(data, dest='en')

    update.message.reply_text('Okay my foodie friend, I will send you U5 Menza foods NOW'+"\n"+data+"\n"+str(en_data))


def start(bot, update):
    update.message.reply_text('Okay my foodie friend, type /get to get the list')


def echo(bot, update):
    update.message.reply_text('Okay my foodie friend, I will send you U5 Menza foods NOW')
    menza = "https://jidelnicek.utb.cz/WebKredit/rss?canteenId=3&language=En"

    d = feedparser.parse(menza)
    data = cleanhtml(d.entries[1]["summary"])


    translator = Translator()

    en_data = translator.translate(data, dest='en')


    update.message.reply_text(data+"\n"+en_data)









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
        dp.add_handler(CommandHandler("get", get))


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
