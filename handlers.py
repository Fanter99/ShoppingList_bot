import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from const import mydb,mycursor, init_menu_buttons, HELP, LIST_BUTTON2
from typing import Union, List

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

'''
if you don't want to see the logs of some class

aps_logger = logging.getLogger('class')
aps_logger.setLevel(lfreogging.WARNING)
'''
def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu

def user_check(user_id: int) -> bool:
    mycursor.execute("select user_id from users where user_id = '%s'" % user_id)
    if mycursor.fetchall():
        return True
    else: return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if user_check(context._user_id):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='user_data: %s' %context.user_data)
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="pls give your first list some name!")
        mycursor.execute("CREATE TABLE %s (list_id varchar(20), item varchar(20))" % "_".join(("user",str(context._user_id))))
        mycursor.execute("INSERT INTO users (user_id, Tabl) VALUES (%d, '%s')" % (context._user_id, "_".join(("user",str(context._user_id)))))
        mydb.commit()
        context.user_data.update({"active_mod": True})
        return 0

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="<b>menu</b>", parse_mode="HTML" ,reply_markup=InlineKeyboardMarkup(build_menu(init_menu_buttons, n_cols=2)))

async def startAdd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if user_check(context._user_id):
        if (context.user_data["active_mod"]):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="you are already in active mod")

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You are now in Active mod. Everything that you type, will automatically added to your default Cart. To leave the active mod type command /leave")
            context.user_data.update({"active_mod": True})


async def leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if user_check(context._user_id):
        context.user_data.update({"active_mod": False})
        await context.bot.send_message(chat_id=update.effective_chat.id, text="you left the active mod")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if user_check(context._user_id):
        if context.user_data["active_mod"]:
            text = update.message.text.lower()
            table = "_".join(("user",str(context._user_id)))
            default = context.user_data["default_list"]
            if default != None:
                mycursor.execute("select item from %s where item = '%s' and list_id = '%s' " % (table, text, default))

                if not mycursor.fetchall():
                    mycursor.execute("INSERT INTO %s (list_id, item) VALUES ('%s', '%s')" % (table, default, text))
                    mydb.commit()
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="%s added to the list" % text)
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="item already exists")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="no default list")

async def show_members(table:str, list:str, context, update):
    mycursor.execute("select item from %s where list_id = '%s' " % (table, list))
    myresult = mycursor.fetchall()
    for i in myresult:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=i[0], reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton("❌", callback_data="delete_button"+"."+list)
]
]))
async def list_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    table = "_".join(("user", str(context._user_id)))
    default = context.user_data["default_list"]
    if default != None:
        await show_members(table,default, context,update)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="no default list")

async def new_list_enter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="please, enter the name for your new list")
    return 0
async def new_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text[0] == '/':
        await context.bot.send_message(chat_id=update.effective_chat.id, text="please, do not use the / symbol in your name")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Try to enter a name for your list one more time:")
        return 0
    else:
        if update.message.text in context.user_data["lists"]:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="list with this name is already exists")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Try to enter a name for your list one more time:")
            return 0
        else:
            context.user_data["lists"].add(text)

            context.user_data.update({"default_list": text})
            await context.bot.send_message(chat_id=update.effective_chat.id, text="new list has been added. it's default now")
            return ConversationHandler.END


async def list_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    default = context.user_data["default_list"]
    if default != None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text= context.user_data["default_list"])
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="no default list")

async def all_list(update:Update, context: ContextTypes.DEFAULT_TYPE):
    if user_check(context._user_id):
        for i in context.user_data["lists"]:
            await context.bot.send_message(chat_id=update.effective_chat.id, text= i)

async def change_default(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        if ' '.join(context.args) in context.user_data['lists']:
            context.user_data.update({"default_list": ' '.join(context.args)})
            await context.bot.send_message(chat_id=update.effective_chat.id, text="default list has been changed!")
        else: await context.bot.send_message(chat_id=update.effective_chat.id, text="no such list")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="please, enter the name for your new default list after the command")

async def changename_Callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    li = context.user_data['change_name_query']
    return await change_list_name_(update, context, li, text)

async def change_list_name_(update: Update, context: ContextTypes.DEFAULT_TYPE, li:str, new_name:str):
    table = "_".join(("user", str(context._user_id)))
    default = context.user_data["default_list"]
    if new_name in context.user_data["lists"]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="list with this name is already exists")
        return 0
    else:
        mycursor.execute("UPDATE %s SET list_id = '%s' WHERE list_id = '%s'" % (table, li, new_name))
        mydb.commit()
        context.user_data["lists"].remove(li)
        context.user_data["lists"].add(new_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="the name for this list has been changed")
        if li == default:
            context.user_data.update({"default_list": new_name})
        return ConversationHandler.END
async def change_list_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    default = context.user_data["default_list"]
    if default != None:
        if context.args:
            await change_list_name_(update, context, default, ' '.join(context.args))
            context.user_data.update({"default_list": ' '.join(context.args)})
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="please, enter the new name for your list after the command")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="no default list")

async def first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    context.user_data.update({"lists": {message}})
    context.user_data.update({"default_list": message})

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Congrats, your first list called: %s" % message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP, parse_mode='HTML')
    return ConversationHandler.END

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text= HELP, parse_mode="HTML")



async def delete_list_(update, context, li):
    table = "_".join(("user", str(context._user_id)))
    context.user_data["lists"].remove(li)

    if li == context.user_data["default_list"]:
        context.user_data.update({"default_list": None})
        await context.bot.send_message(chat_id=update.effective_chat.id, text="this was your default list, there is no default list now")
    mycursor.execute("DELETE FROM %s WHERE list_id = '%s' " % (table, li))
    mydb.commit()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="the list has been deleted")
async def delete_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    li = ' '.join(context.args)

    if context.args:
        if li in context.user_data["lists"]:
            await delete_list_(update, context, li)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="there is no such list")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="please, enter the new name for the list to be deleted")

async def delete_(table, li, item:str):
    mycursor.execute("DELETE FROM %s WHERE item = '%s' and list_id = '%s' " % (table, item, li))
    mydb.commit()
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    table = "_".join(("user", str(context._user_id)))
    default = context.user_data["default_list"]
    mycursor.execute("select item from %s where list_id = '%s' " % (table, default))
    myresult = mycursor.fetchall()
    if context.args:
        if ' '.join(context.args) in myresult:
            for i in context.args:
                await delete_(table,default,i)

            await delete_(table,default, ' '.join(context.args))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="item(s) has been removed from the list")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="no such element in this list")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="please, enter the member to be deleted")

async def cancel(update: Update, context = ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.")
    return ConversationHandler.END

async def changenameQuery_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("changenameQuery_handler")
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="please, enter the new name for your list")
    context.user_data.update({'change_name_query': query.data.partition('.')[2]})
    return 0

async def newListQuery_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("newListQuery_handler")
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="please, enter the name for your new list")
    return 0

async def deleteQuery_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("deleteQuery_handler")
    table = "_".join(("user", str(context._user_id)))
    query = update.callback_query
    await query.answer()

    await delete_(table,query.data.partition('.')[2],query.message.text)
    await query.delete_message()

async def menuQuery_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("menuQuery_handler")
    table = "_".join(("user", str(context._user_id)))
    default = context.user_data["default_list"]
    query = update.callback_query
    await query.answer()
    async def lists_help():
        button_list = [InlineKeyboardButton(i, callback_data=i) for i in list(context.user_data["lists"])]
        button_list.append(InlineKeyboardButton("GO BACK", callback_data="back_menu"))
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
        await query.edit_message_text(text='<b>menu</b>', parse_mode='HTML', reply_markup=reply_markup)
    match query.data.partition('.')[0]:
        case "back_lists":
            await lists_help()
        case "back_menu":
            await query.edit_message_text(text="<b>menu</b>", parse_mode="HTML",reply_markup=InlineKeyboardMarkup(build_menu(init_menu_buttons, n_cols=2)))
        case "all_lists":
            await lists_help()
        case "current_list":
            if default!= None:
                button_list = [InlineKeyboardButton(i, callback_data=".".join((i, default))) for i in LIST_BUTTON2]
                button_list.append(InlineKeyboardButton("GO BACK", callback_data="back_menu"))
                reply_markup = build_menu(button_list, n_cols=2)
                await query.edit_message_text(text=default + ":", reply_markup=InlineKeyboardMarkup(inline_keyboard=reply_markup))
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="no default list")
        case "show members":
            await show_members(table, query.data.partition('.')[2], context, update)
        case "delete":
            await delete_list_(update,context, query.data.partition('.')[2])
            await lists_help()
        case "change to default":
            context.user_data.update({"default_list":query.data.partition('.')[2]})
            await context.bot.send_message(chat_id=update.effective_chat.id, text="default list has been changed!")
        case _:
            if query.data in context.user_data["lists"]:
                '''def flatten(l):
                    return [item for sublist in l for item in sublist]
'''
                button_list = [InlineKeyboardButton(i, callback_data=".".join((i,query.data))) for i in LIST_BUTTON2]
                button_list.append(InlineKeyboardButton("GO BACK", callback_data="back_lists"))
                markup = build_menu(button_list, n_cols=2)
                await query.edit_message_text(text=query.data+":", reply_markup=InlineKeyboardMarkup(inline_keyboard=markup))

            else: logging.warning("something went so fucking wrong")
            logging.info(update.callback_query.data)
            logging.info("edge")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
