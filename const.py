from db import db
from telegram import InlineKeyboardButton

HELP = "You can control me by sending commands or with help of attachment menu,that you can call by typing /menu in the chat\n\n<b>Some stuff</b>\n\n" \
       "•/menu - show the menu with buttons to control the bot (alternative to command mode)\n" \
       "•/list - show list members\n" \
       "•/all_list - show all list\n" \
       "•/change_default &lt;list-name&gt; - change the default list, where elements will be added\n" \
       "\n<b>List control</b>\n\n" \
       "•/delete &lt;element-name&gt; - delete one element or many elements from a list\n" \
       "•/change_name &lt;new-name&gt; - change a name of a list\n" \
       "•/list_name - name of a current list\n" \
       "•/delete_list &lt;list-name&gt; - delete a list\n" \
       "\n<b>Active mod</b>\nper default you can add elements to a list just by typing them in chat\n\n" \
       "•/leave - disable adding function\n" \
       "•/add - enable adding function" \
       "\n\nif you started a dialog with bot you can always leave it with the /cancel command"

mydb = db().connect("localhost", "root", "root", "telegram_test")
mycursor = mydb.cursor()

init_menu_buttons = [
    InlineKeyboardButton("all lists", callback_data="all_lists"),
    InlineKeyboardButton("current list", callback_data="current_list"),
    InlineKeyboardButton("new list", callback_data="new_list.boba"),
]
LIST_BUTTON2 = ["show members", "delete", "change name", "change to default"]