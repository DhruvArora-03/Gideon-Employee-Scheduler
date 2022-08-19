# telegram imports
API_TOKEN = '5350627481:AAH3m0Nw9JQJ9ShkoZaZ5T_TknXiZ9OUVwI'

from bdb import effective
import logging
from telegram import Update
from telegram.ext import Filters, Updater, MessageHandler, CallbackContext, CommandHandler

import db_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# handle clearChat command
def clearChat(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="clearing..." + "\n"*100 + "chat cleared"
    )

# handle start command
def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hey there, welcome to the team! Use the /help command for a list of commands."
    )
    print(update.effective_user.first_name)
    print(update.effective_user.last_name)
    print(update.effective_user.id)
    db_handler.create_employee(update.effective_user.first_name, update.effective_user.last_name, update.effective_user.id)

# handle help command
def help(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            '/settings - edit settings\n'
            '/help - show this message\n'
            '/viewshifts - view upcoming shifts\n'
            '/cancelshift - cancel a shift'
        )
    )

# handle settings command
def settings(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="No editable settings yet"
    )

# handle viewshifts command
def viewshifts(update: Update, context: CallbackContext):
    shifts = db_handler.get_all_shifts_for_employee(update.effective_user.id)

    if len(shifts) == 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are not currently scheduled to work any upcoming shifts"
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are currently scheduled to work the following shifts:"
        )
        for shift in shifts:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=shift
            )
            

# handle cancelshift command - TODO
def cancelshift(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Cancel a shift by typing the command in this format: \n\"/cancelshift [DATE]\"\nFor instance, to cancel a shift for April 20th, 2022 you would say: \"/cancelshift 2022-04-20\""
        )
    else:
        if db_handler.delete_shift(context.args[0], update.effective_user.id):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Shift successfully canceled."
            )
        else: 
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are not scheduled for any shifts on {}.".format(context.args[0])
            )


# handle non-command messages
def respond_to_non_command(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Sorry, I don't respond to non-command messages. Check out the /help command for a list of commands"
    )

if __name__ == '__main__':
    updater = Updater(API_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # create handlers
    handlers = [
        CommandHandler('clearChat', clearChat),
        CommandHandler('start', start),
        CommandHandler('help', help),
        CommandHandler('settings', settings),
        CommandHandler('viewshifts', viewshifts),
        CommandHandler('cancelshift', cancelshift),
        MessageHandler(Filters.text & ~Filters.command, respond_to_non_command), # only on msgs w no commands
    ]

    # add handlers to application
    for handler in handlers:
        dispatcher.add_handler(handler)
    

    updater.start_polling()
    updater.idle()


