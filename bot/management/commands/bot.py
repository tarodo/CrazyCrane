import logging
import os
from abc import ABC
from enum import Enum, auto

from django.core.management.base import BaseCommand
from telegram import Bot, Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater, CallbackContext)
from telegram.utils.request import Request

from bot.models import Producer

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

request = Request(connect_timeout=0.5, read_timeout=1.0)
bot = Bot(
    request=request,
    token=TELEGRAM_TOKEN,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class States(Enum):
    START = auto()
    PRODUCER = auto()


def keyboard_row_divider(full_list, row_width=2):
    """Divide list into rows for keyboard"""
    for i in range(0, len(full_list), row_width):
        yield full_list[i: i + row_width]


def send_first_question(update: Update, context: CallbackContext) -> States:
    buttons = ['Хочу найти кран', 'Какие есть краны?']
    reply_keyboard = list(keyboard_row_divider(buttons))
    update.message.reply_text(
        'Вот ду ю вонт?:',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
    return States.START


def start(update: Update, context: CallbackContext) -> States:
    user = update.message.from_user
    update.message.reply_text("Hello my friend")
    logger.info(f"User {user.first_name} :: {user.id} started the conversation.")

    return send_first_question(update, context)


def send_producers(update: Update, context: CallbackContext) -> States:
    producers = Producer.objects.all()
    buttons = [producer.name for producer in producers]
    reply_keyboard = list(keyboard_row_divider(buttons))
    update.message.reply_text(
        'Есть такие производители:',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
    return States.PRODUCER


def choose_game(update: Update, context: CallbackContext) -> States:
    user_text = update.message.text
    update.message.reply_text(f"Вы сказали `{user_text}`\nПростите, это слишком сложно для меня")
    if Producer.objects.count() > 0:
        return send_producers(update, context)

    return send_first_question(update, context)


def cancel(update: Update, _) -> int:
    """Cancel and end the conversation."""
    user = update.message.from_user
    logger.info('User %s canceled the conversation.', user.first_name)
    update.message.reply_text(
        'Всего доброго!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


class Command(BaseCommand, ABC):
    """Start the bot."""

    help = "Телеграм-бот"
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
        ],
        states={
            States.START: [
                MessageHandler(Filters.text & ~Filters.command, choose_game),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
        ],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
