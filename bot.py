# telegram imports
API_TOKEN = '5350627481:AAH3m0Nw9JQJ9ShkoZaZ5T_TknXiZ9OUVwI'

from bdb import effective
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CallbackContext, CommandHandler

import database_handler as db_hand

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# handle clearChat command
async def clearChat(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="clearing..." + "\n"*100 + "chat cleared"
    )

# handle start command
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hey there, welcome to the team! Use the /help command for a list of commands."
    )
    print(update.effective_user.first_name)
    print(update.effective_user.last_name)
    print(update.effective_user.id)
    db_hand.create_employee(update.effective_user.first_name, update.effective_user.last_name, update.effective_user.id)

# handle help command
async def help(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            '/settings - edit settings\n'
            '/help - show this message\n'
            '/viewshifts - view upcoming shifts\n'
            '/cancelshift - cancel a shift'
        )
    )

# handle settings command
async def settings(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="No editable settings yet"
    )

# handle viewshifts command - TODO
async def viewshifts(update: Update, context: CallbackContext.DEFAULT_TYPE):
    # TODO: get shifts from database
    shifts = list()

    if len(shifts) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are not currently scheduled to work any upcoming shifts"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are currently scheduled to work the following shifts:\n" + "\n".join(shifts)
        )

# handle cancelshift command - TODO
async def cancelshift(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Enter the ID number of the shift you want to cancel. Check out the /viewshifts command to find the ID number"
    )

# handle non-command messages
async def respond_to_non_command(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Sorry, I don't respond to non-command messages. Check out the /help command for a list of commands"
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_TOKEN).build()
    
    # create handlers
    handlers = [
        CommandHandler('clearChat', clearChat),
        CommandHandler('start', start),
        CommandHandler('help', help),
        CommandHandler('settings', settings),
        CommandHandler('viewshifts', viewshifts),
        CommandHandler('cancelshift', cancelshift),
        MessageHandler(filters.TEXT, respond_to_non_command), # only on msgs w no commands
    ]

    # add handlers to application
    for handler in handlers:
        application.add_handler(handler)
    

    application.run_polling(stop_signals=None)


