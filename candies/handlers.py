from telegram import Update, ReplyKeyboardMarkup #, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler,\
        MessageHandler, Filters

from candies.model import setTotalCandies, setMaxDecr, getTotalCandies, getMaxDecr,\
        botTurn, playerTurn

(
    TOTAL_CANDIES_STATE,
    MAX_DECR_STATE,
    FIRST_TURN_STATE,
    PLAYER_TURN_STATE
) = range(4)


def initCandiesConversation (dispatcher) -> None:
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('candies', candiesCommand)],
        states={
            TOTAL_CANDIES_STATE: [MessageHandler(Filters.text, inputTotalCandiesHandler)],
            MAX_DECR_STATE: [MessageHandler(Filters.text, inputMaxDecrHandler)],
            FIRST_TURN_STATE: [MessageHandler(Filters.text, inputFirstTurnHandler)],
            PLAYER_TURN_STATE: [MessageHandler(Filters.text, playerTurnHandler)],
        },
        fallbacks=[],
    ))


def candiesCommand(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Игра в конфеты" +
            "\nВведите начальное количество конфет:")
    return TOTAL_CANDIES_STATE


def inputTotalCandiesHandler(update: Update, context: CallbackContext) -> int:
    userInput = update.message.text
    
    if not userInput.isdigit() or int(userInput) <= 0:
        update.message.reply_text("Вы должны ввести натуральное число." +
            "\nВведите начальное количество конфет:")
        return TOTAL_CANDIES_STATE
    
    setTotalCandies(int(userInput))
    
    update.message.reply_text("Введите, сколько можно максимально брать конфет:")
    return MAX_DECR_STATE


def inputMaxDecrHandler(update: Update, context: CallbackContext) -> int:
    userInput = update.message.text
    
    if not userInput.isdigit() or int(userInput) <= 0:
        update.message.reply_text("Вы должны ввести натуральное число." +
            "\nВведите, сколько можно максимально брать конфет:")
        return MAX_DECR_STATE
        
    if int(userInput) > getTotalCandies():
        update.message.reply_text("Число не должно превышать начальное количество конфет." +
            "\nВведите, сколько можно максимально брать конфет:")
        return MAX_DECR_STATE
    else: setMaxDecr(int(userInput))

    replyMarkup = ReplyKeyboardMarkup([
        ["Я, бот", "Вы, игрок"],
    ], resize_keyboard=True, one_time_keyboard=True)

    # replyMarkup = InlineKeyboardMarkup(
    #     [[
    #         InlineKeyboardButton("Я, бот", callback_data='bot'),
    #         InlineKeyboardButton("Вы, игрок", callback_data='player')]]
    # )
    
    update.message.reply_text("Кто будет ходить первым?", reply_markup=replyMarkup)
    return FIRST_TURN_STATE


def inputFirstTurnHandler(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Начинаем игру")

    if update.message.text == 'bot':
        if botTurnOutput(update):
            return ConversationHandler.END

    update.message.reply_text("Сколько возьмёте конфет?")
    
    return PLAYER_TURN_STATE


def playerTurnHandler(update: Update, context: CallbackContext) -> int:
    userInput = update.message.text
    
    if not userInput.isdigit() or int(userInput) <= 0:
        update.message.reply_text("Вы должны ввести натуральное число." +
            "\nСколько возьмёте конфет?")
        return PLAYER_TURN_STATE
    
    decr = int(userInput)
    if decr > getMaxDecr() or decr > getTotalCandies():
        update.message.reply_text("Так много конфет взять нельзя." +
            "\nСколько возьмёте конфет?")
        return PLAYER_TURN_STATE
    
    playerTurn(decr)

    if not getTotalCandies():
        update.message.reply_text("Игра закончена. Вы выиграли. Поздравляю!")
        return ConversationHandler.END
        
    if botTurnOutput(update):
        return ConversationHandler.END

    update.message.reply_text("Сколько возьмёте конфет?")

    return PLAYER_TURN_STATE


# Возвращает True, если игра закончена
def botTurnOutput(update: Update):
    decr = botTurn()
    
    if not getTotalCandies():
        update.message.reply_text(f"Я взял {decr} конфет\nИгра закончена. Я выиграл")
        return True
    else:
        update.message.reply_text(f"Я взял {decr} конфет\nОсталось {getTotalCandies()}")
        return False