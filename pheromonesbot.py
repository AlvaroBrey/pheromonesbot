#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pheromones Bot

import logging
from datetime import datetime
import pytz
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

TIMEZONE_STR = 'Europe/Kiev'
TIMEZONE = pytz.timezone(TIMEZONE_STR)
TYPES_MAP = {
    0: "Wind",
    1: "Water",
    2: "Fire",
    3: "Earth",
    4: "Arcana",
    5: "Earth",
    6: "Earth"
}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def pheromones(bot, update):
    weekday = TIMEZONE.localize(datetime.utcnow()).weekday()
    spawn = TYPES_MAP.get(weekday)
    logger.debug('Called with weekday %d and spawn %s' % (weekday, spawn))
    update.message.reply_text(
        "Pheromones spawn is currently *%s*." % spawn,
        parse_mode=ParseMode.MARKDOWN)


def help(bot, update):
    update.message.reply_text(
        'Usage: /pheromones', quote=True)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():

    with open("bot_id.txt", "r") as token_file:
        bot_token = token_file.read()
        updater = Updater(bot_token)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("pheromones", pheromones))

        dp.add_handler(CommandHandler("help", help))

        # log all errors
        dp.add_error_handler(error)

        # Start the Bot
        updater.start_polling()

        logger.debug("Bot up!")

        updater.idle()


if __name__ == '__main__':
    main()
