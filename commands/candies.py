# Define a few command handlers. These usually take the two arguments update and context
from telegram import Update
from telegram.ext import CallbackContext

from handlers import ALL_NUM_STATE

def candiesCommand(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(f"Игра в конфеты")

    update.message.reply_text(f"Введите начальное количество конфет:")
    return ALL_NUM_STATE

# def candiesConvInit(dispatcher) -> None:
#     candiesConvHandler = ConversationHandler(
#         entry_points=[CommandHandler('candies', candiesCommand)],
#         states={
#             ALL_NUM_STATE: [MessageHandler(Filters.text, inputAllNumHandler)],
#             DECR_NUM_STATE: [MessageHandler(Filters.text, inputDecrNumHandler)],
#             PLAYER_TURN_STATE: [MessageHandler(Filters.text, playerTurnHandler)],
#         },
#         fallbacks=[],
#     )
#     dispatcher.add_handler(candiesConvHandler)
