import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from commands import *
from handlers import *
# from handlers.candies import input_player_name_handler, input_player_age_handler, PLAYER_NAME_STATE, \
#     PLAYER_AGE_STATE, PLAYER_GENDER_STATE, input_player_gender_handler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "5655208234:AAHXRiFZdXwcPN9GleFwA7LA6S-vWdUBfWo"


def main() -> None:
    """Start the bot."""

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("candies", candiesCommand))
    candiesConvHandler = ConversationHandler(
        entry_points=[CommandHandler('candies', candiesCommand)],
        states={
            ALL_NUM_STATE: [MessageHandler(Filters.text, inputAllNumHandler)],
            DECR_NUM_STATE: [MessageHandler(Filters.text, inputDecrNumHandler)],
            PLAYER_TURN_STATE: [MessageHandler(Filters.text, playerTurnHandler)],
        },
        fallbacks=[],
    )
    dispatcher.add_handler(candiesConvHandler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()