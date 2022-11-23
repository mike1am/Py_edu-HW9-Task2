from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters

candiesNum = 0
maxDecr = 0

(
    ALL_NUM_STATE,
    DECR_NUM_STATE,
    PLAYER_TURN_STATE
) = range(3)


def initCandiesConversation (dispatcher) -> None:
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('candies', candiesCommand)],
        states={
            ALL_NUM_STATE: [MessageHandler(Filters.text, inputAllNumHandler)],
            DECR_NUM_STATE: [MessageHandler(Filters.text, inputDecrNumHandler)],
            PLAYER_TURN_STATE: [MessageHandler(Filters.text, playerTurnHandler)],
        },
        fallbacks=[],
    ))


def candiesCommand(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Игра в конфеты" +
            "\nВведите начальное количество конфет:")
    return ALL_NUM_STATE


def inputAllNumHandler(update: Update, context: CallbackContext) -> int:
    userInput = update.message.text
    
    if not userInput.isdigit() or int(userInput) <= 0:
        update.message.reply_text("Вы должны ввести натуральное число." +
            "\nВведите начальное количество конфет:")
        return ALL_NUM_STATE
    
    global candiesNum
    candiesNum = int(userInput)
    
    update.message.reply_text("Введите, сколько можно максимально брать конфет:")
    return DECR_NUM_STATE


def inputDecrNumHandler(update: Update, context: CallbackContext) -> int:
    userInput = update.message.text
    
    if not userInput.isdigit() or int(userInput) <= 0:
        update.message.reply_text("Вы должны ввести натуральное число." +
            "\nВведите, сколько можно максимально брать конфет:")
        return DECR_NUM_STATE
        
    global maxDecr
    maxDecr = int(userInput)
    if maxDecr > candiesNum:
        update.message.reply_text("Число не должно превышать начальное количество конфет." +
            "\nВведите, сколько можно максимально брать конфет:")
        return DECR_NUM_STATE

    update.message.reply_text("Начинаем игру.\nСколько возьмёте конфет?")
    return PLAYER_TURN_STATE


def playerTurnHandler(update: Update, context: CallbackContext) -> int:
    userInput = update.message.text
    
    if not userInput.isdigit() or int(userInput) <= 0:
        update.message.reply_text("Вы должны ввести натуральное число." +
            "\nСколько возьмёте конфет?")
        return PLAYER_TURN_STATE
    
    global candiesNum, decrNum
    decr = int(userInput)
    if decr > maxDecr or decr > candiesNum:
        update.message.reply_text("Так много конфет взять нельзя." +
            "\nСколько возьмёте конфет?")
        return PLAYER_TURN_STATE
    
    candiesNum -= decr

    if not candiesNum:
        update.message.reply_text("Игра закончена.")
        return ConversationHandler.END

    update.message.reply_text(f"Осталось {candiesNum} конфет.\nСколько возьмёте конфет?")
    return PLAYER_TURN_STATE