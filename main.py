from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, PicklePersistence, CallbackQueryHandler, Updater
from handlers import *
import handlers
import os
def main():

    TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
    my_persistence = PicklePersistence(filepath='persistence')
    application = ApplicationBuilder().token(TOKEN).persistence(persistence=my_persistence).concurrent_updates(False).build()

    add_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), add)
    startAdd_handler = CommandHandler('add', startAdd)
    leave_handler = CommandHandler('leave', leave)
    list_handler = CommandHandler('list', list_)
    delete_handler = CommandHandler('delete', delete)
    menu_handler = CommandHandler('menu', menu)
    help_handler = CommandHandler('help', help)
    changeListname_handler = CommandHandler('change_name', change_list_name)
    allList_handler = CommandHandler('all_list', all_list)
    listName_handler = CommandHandler('list_name', list_name)
    changeDefault_handler = CommandHandler('change_default', change_default)
    deleteList_handler = CommandHandler('delete_list', delete_list)

    shared_handler = MessageHandler(filters.StatusUpdate.USER_SHARED, handlers.shared_handler)
    menuQuery_handler = CallbackQueryHandler(handlers.menuQuery_handler)

    deleteQuery_handler = CallbackQueryHandler(handlers.deleteQuery_handler, pattern="^delete_button")
    shareQuery_handler = CallbackQueryHandler(handlers.shareQuery_handler, pattern='^SHARE')
    start_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            0: [MessageHandler(filters.TEXT & (~filters.COMMAND), first_name),

                ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    newList_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("new_list", new_list_enter), CallbackQueryHandler(newListQuery_handler, pattern="^new_list")],
        states={
            0: [MessageHandler((filters.TEXT | filters.COMMAND)& (~filters.Text(['/cancel'])) , new_list),
                ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    changeName_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(changenameQuery_handler, pattern="^change name")],
        states={
            0: [MessageHandler((filters.TEXT | filters.COMMAND) & (~filters.Text(['/cancel'])), changename_Callback),
                ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(deleteList_handler)
    application.add_handler(changeName_conv_handler)
    application.add_handler(start_conv_handler)
    application.add_handler(newList_conv_handler)
    application.add_handler(changeListname_handler)
    application.add_handler(allList_handler)
    application.add_handler(list_handler)
    application.add_handler(leave_handler)
    application.add_handler(delete_handler)
    application.add_handler(startAdd_handler)
    application.add_handler(menu_handler)
    application.add_handler(help_handler)
    application.add_handler(add_handler)
    application.add_handler(listName_handler)
    application.add_handler(changeDefault_handler)
    application.add_handler(shared_handler)
    application.add_handler(shareQuery_handler)
    application.add_handler(deleteQuery_handler)
    application.add_handler(menuQuery_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
