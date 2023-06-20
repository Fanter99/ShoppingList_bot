from db import db
from telegram import InlineKeyboardButton

HELP = "You can control me by sending commands or with help of attachment menu,that you can call by typing /menu in the chat\n\n<b></b>\n\n" \
       "\n<b>Adding to a list</b>\n\n" \
       "you can add something to a default list just by typing it in chat\n" \
       "you must always have a list, where you want new elements to be as your default\n" \
       "to change a default list use /change_default or just simply use an attachment menu with the /menu command\n" \
       "\n<b>List control</b> (or use a /menu instead)\n\n" \
       "•/list - show members of a default list\n" \
       "•/all_list - show all lists\n" \
       "•/delete &lt;element-name&gt; - delete one element from a default list\n" \
       "•/change_name &lt;new-name&gt; - change a name of a default list\n" \
       "•/list_name - name of a current list\n" \
       "•/delete_list &lt;list-name&gt; - delete a default list\n" \
       "•/change_default &lt;list-name&gt; - change the default list, where elements will be added\n" \
       "\n<b>Active mod</b>\n\nyou can add elements to a default list just by typing them in chat\n\n" \
       "•/leave - disable adding function\n" \
       "•/add - enable adding function" \
       "\n\nif you started a dialog with bot you can always leave it with the /cancel command"

mydb = db().connect("localhost", "root", "root", "telegram_test")
mycursor = mydb.cursor()

init_menu_buttons = [
    InlineKeyboardButton("all lists", callback_data="all_lists"),
    InlineKeyboardButton("current list", callback_data="current_list"),
    InlineKeyboardButton("new list", callback_data="new_list"),
]
LIST_BUTTON2 = ["show members", "delete", "change name", "change to default", "SHARE"]