from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

candiesNum = 0
maxDecr = 0

(
    ALL_NUM_STATE,
    DECR_NUM_STATE,
    PLAYER_TURN_STATE
) = range(3)


# inputAllNumHandler, inputDecrNumHandler, playerTurnHandler
def inputAllNumHandler(update: Update, context: CallbackContext) -> int:
    userInput = update.message.text
    
    if not userInput.isdigit() or int(userInput) <= 0:
        update.message.reply_text("Вы должны ввести натуральное число.")
        return ALL_NUM_STATE
    
    global candiesNum
    candiesNum = int(userInput)
    
    update.message.reply_text("Введите, сколько можно максимально брать конфет:")
    return DECR_NUM_STATE


def inputDecrNumHandler(update: Update, context: CallbackContext) -> int:
    userInput = update.message.text
    
    if not userInput.isdigit() or int(userInput) <= 0:
        update.message.reply_text("Вы должны ввести натуральное число.")
        return DECR_NUM_STATE
        
    global maxDecr
    maxDecr = int(userInput)
    if maxDecr > candiesNum:
        update.message.reply_text("Число не должно превышать начальное количество конфет.")
        return DECR_NUM_STATE

    update.message.reply_text("Начинаем игру.\nСколько возьмёте конфет?")
    return PLAYER_TURN_STATE


def playerTurnHandler(update: Update, context: CallbackContext) -> int:
    userInput = update.message.text
    
    if not userInput.isdigit() or int(userInput) <= 0:
        update.message.reply_text("Вы должны ввести натуральное число.")
        return PLAYER_TURN_STATE
    
    global candiesNum, decrNum
    decr = int(userInput)
    if decr > maxDecr or decr > candiesNum:
        update.message.reply_text("Вы ввели слишком большое количество конфет.")
        return PLAYER_TURN_STATE
    
    candiesNum -= decr

    if not candiesNum:
        update.message.reply_text("Игра закончена.")
        return ConversationHandler.END

    update.message.reply_text(f"Осталось {candiesNum} конфет.\nСколько возьмёте конфет?")
    return PLAYER_TURN_STATE