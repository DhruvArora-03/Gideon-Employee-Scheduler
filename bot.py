# telegram imports
API_TOKEN = '5350627481:AAH3m0Nw9JQJ9ShkoZaZ5T_TknXiZ9OUVwI'

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
    if db_handler.is_manager(update.effective_chat.id):
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            'Manager-only comamnds:\n\n'
            '/createshift - create a new shift\n'
            '/deleteshift - delete an existing shift'
            '/populateshift - populate a shift with employees'
            '/listshifts - list all shifts'
        )
    )

# # handle settings command
# def settings(update: Update, context: CallbackContext):
#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text="No editable settings yet"
#     )

# # handle viewshifts command
# def viewshifts(update: Update, context: CallbackContext):
#     shifts = db_handler.get_all_shifts_for_employee(update.effective_user.id)

#     if len(shifts) == 0:
#         context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text="You are not currently scheduled to work any upcoming shifts"
#         )
#     else:
#         context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text="You are currently scheduled to work the following shifts:"
#         )
#         for shift in shifts:
#             context.bot.send_message(
#                 chat_id=update.effective_chat.id,
#                 text=shift
#             )
            

# # handle cancelshift command - TODO
# def cancelshift(update: Update, context: CallbackContext):
#     if len(context.args) == 0:
#         context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text="Cancel a shift by typing the command in this format: \n\"/cancelshift [DATE]\"\nFor instance, to cancel a shift for April 20th, 2022 you would say: \"/cancelshift 2022-04-20\""
#         )
#     else:
#         if db_handler.delete_shift(context.args[0], update.effective_user.id):
#             context.bot.send_message(
#                 chat_id=update.effective_chat.id,
#                 text="Shift successfully canceled."
#             )
#         else: 
#             context.bot.send_message(
#                 chat_id=update.effective_chat.id,
#                 text="You are not scheduled for any shifts on {}.".format(context.args[0])

# MANAGER ONLY COMMANDS:

# handle promoteself command
def promoteself(update: Update, context: CallbackContext):
    if not db_handler.is_manager(update.effective_user.id):
        db_handler.promote_employee(update.effective_user.id)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You have been promoted to manager!"
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are already a manager."
        )

# handle createshift command
def createshift(update: Update, context: CallbackContext):
    '''
    createshift: handle the /createshift command which asks the user for 7 params 
                to create a new shift.
                
                /createshift [MONTH] [DAY] [YEAR] [HOUR] [MINUTE] [LENGTH] [# OF STAFF]

    Args:
        update (Update): _description_
        context (CallbackContext): _description_
    '''
    if not db_handler.is_manager(update.effective_chat.id):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='You do not have permission to run this command'
        )
    elif len(context.args) != 7: # month, day, year, hour, minute, length, staff
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "Create a shift by typing the command in this format: \n\n"
                "\"/createshift [MONTH] [DAY] [YEAR] [HOUR] [MINUTE] [SHIFT LENGTH] [# STAFF]\"\n\n"
                "For instance, to create a shift for 4-20-2022, 3:30 PM to 7 PM, with 3 employees you would say: \n\n"
                "\"/createshift 4 20 2022 15 30 3.5 3\""
            )
        )
    else:
        args = [int(context.args[i]) if i != 5 else float(context.args[i]) for i in range(7)]
        print('Creating shift with args:', args)
        args.append(update.effective_user.id)
        db_handler.create_shift(*args)
        print('Shift created')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Shift successfully created."
        )


# handle deleteshift command
def deleteshift(update: Update, context: CallbackContext):
    pass # TODO

# handle populateshift command
def populateshift(update: Update, context: CallbackContext):
    if not db_handler.is_manager(update.effective_chat.id):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='You do not have permission to run this command'
        )
    elif len(context.args) != 1: # shift id
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "Populate a shift by typing the command in this format: \n\n"
                "\"/populateshift [SHIFT ID]\"\n\n"
                "You can find shift IDs by running the /viewshifts command."
            )
        )
    else:
        shift_id = int(context.args[0])
        if db_handler.populate_shift(shift_id):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Shift successfully populated."
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Shift could not be populated. Use /shiftdetails to see more info."
            )

# handle listshifts command
def listshifts(update: Update, context: CallbackContext):
    if not db_handler.is_manager(update.effective_chat.id):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='You do not have permission to run this command'
        )
    else:
        shifts = db_handler.get_all_shifts()
        if len(shifts) == 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="There are no upcoming shifts."
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="The following shifts are currently scheduled:"
            )
            for shift in shifts:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=shift
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
        # CommandHandler('settings', settings),
        # CommandHandler('viewshifts', viewshifts),
        # CommandHandler('cancelshift', cancelshift),
        CommandHandler('promoteself', promoteself),
        CommandHandler('createshift', createshift),
        CommandHandler('populateshift', populateshift),
        MessageHandler(Filters.text & ~Filters.command, respond_to_non_command), # only on msgs w no commands
    ]

    # add handlers to application
    for handler in handlers:
        dispatcher.add_handler(handler)
    

    updater.start_polling()
    updater.idle()


