#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Pheromones Bot

import logging
import calendar
from datetime import datetime, timedelta, timezone
import pytz import timezone
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

TIMEZONE_STR = 'Europe/Kiev'
TIMEZONE = timezone(TIMEZONE_STR)
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


def get_ukraine_datetime():
    return datetime.now(TIMEZONE)


def time_until_end_of_day():
    dt = get_ukraine_datetime()
    tomorrow = dt + timedelta(days=1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month,
                        day=tomorrow.day, hour=0, minute=0, second=0)
    midnight = TIMEZONE.localize(midnight)
    return midnight - dt


def format_timedelta(delta):
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    return '%d hours, %d minutes and %d seconds' % (hours, minutes, seconds)


def pheromones(bot, update):
    weekday = get_ukraine_datetime().weekday()
    spawn = TYPES_MAP.get(weekday)
    logger.debug('Called with weekday %d and spawn %s' % (weekday, spawn))
    update.message.reply_text(
        "Pheromones spawn type is currently *%s*. Spawn changes in %s." % (
            spawn, format_timedelta(time_until_end_of_day)),
        parse_mode=ParseMode.MARKDOWN)


def list(bot, update):
    msg = ""
    for key, value in TYPES_MAP.items():
        msg += "%s: %s\n" % (calendar.day_name[key], value)
    update.message.reply_text(msg)


def help(bot, update):
    update.message.reply_text(
        'Usage: /pheromones', quote=True)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():

    with open("bot_id.txt", "r") as token_file:
        bot_token = token_file.read().replace('\r', '').replace('\n', '')
        updater = Updater(bot_token)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("pheromones", pheromones))

        dp.add_handler(CommandHandler("list", list))

        dp.add_handler(CommandHandler("help", help))

        # log all errors
        dp.add_error_handler(error)

        # Start the Bot
        updater.start_polling()

        logger.debug("Bot up!")

        updater.idle()


if __name__ == '__main__':
    main()
