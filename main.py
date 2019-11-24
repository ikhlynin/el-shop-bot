import logging
import telegram
import datetime
 
from telegram import Bot
from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
 
TOKEN = '933557239:AAEzIKCT4VYB0kJt92Ep3ZPuM1sDYsHrG6U'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
 
 
def reply_keyboard():
    keyboard = [
        [
            KeyboardButton('Каталог'),
            KeyboardButton('Контакты'),
            KeyboardButton('FAQ'),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
 
# keayboard for FAQ
 
 
def faq_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Прайслист", callback_data="price")
        ],
        [
            InlineKeyboardButton("Доставка", callback_data="shipping")
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
 
 
def faq(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Частые вопросы',
        reply_markup=faq_keyboard()
    )
 
    ### REWRITE ###
# keyboeard for catalog
 
 
def inline_keyboard(id):
    keyboard = [
        [
            InlineKeyboardButton("Купить", callback_data="buy_"+id),
            InlineKeyboardButton("Посмотреть", callback_data="view_"+id)
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
 
 
def catalog(update, context, id, src, ctext):
    context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo=open(src, 'rb')
    )
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=ctext,
        reply_markup=inline_keyboard(id)
    )
 
    ### REWRITE ###
 
 
# contacts
def contacts(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Почта: elShop@devs.com\nТелефон: 380508409843'
    )
# menu
 
# comand /start
 
 
def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Привет! Здесь ты можешь купить различные игры фильмы и книги в цифровом варианте.',
        reply_markup=reply_keyboard()
    )
 
 
# listner
def echo(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    if text == 'Каталог':
        catalog(update, context, "1", "img/Joker/poster.jpg", 'Joker\nForever alone in a crowd, failed comedian Arthur Fleck seeks connection as he walks the streets of Gotham City\n2019 год\n20$')
        catalog(update, context, "2", "img/Godfather/poster.jpg", 'Joker\nDon Vito Corleone, head of a mafia family, decides to handover his empire to his youngest son Michael. However, his decision unintentionally puts the lives of his loved ones in grave danger.\n1979 год\n10$')
    if text == 'FAQ':
        return faq(update, context)
    if text == 'Контакты':
        return contacts(update, context)
    
 
def keyboard_callback_handler(update, context):
    print("Я тут")
    query = update.callback_query
    data = query.data
    now = datetime.datetime.now()
 
    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text
 
    print(data.split("_")[0])
 
    if data == "shipping":
        context.bot.send_message(
            chat_id=chat_id,
            text='Доставка моментальная, это же электронные товары)',
        )
    if data == "price":
        context.bot.send_document(
            chat_id=chat_id,
            document=open('docs/price-list.txt', 'rb')
        )
    if data.split("_")[0] == "view":
        if data.split("_")[1] == "1":
            context.bot.send_photo(
                chat_id=chat_id,
                photo=open('img/Joker/joker1.jpg', 'rb')
            )
            context.bot.send_photo(
                chat_id=chat_id,
                photo=open('img/Joker/joker2.jpg', 'rb')
            )
        elif data.split("_")[1] == "2":
            context.bot.send_photo(
                chat_id=chat_id,
                photo=open('img/Godfather/gf1.jpg', 'rb')
            )
            context.bot.send_photo(
                chat_id=chat_id,
                photo=open('img/Godfather/gf2.jpg', 'rb')
            )

    if data.split("_")[0] == "buy":
        name = update.effective_user.username
        if data.split("_")[1] == "1":
           context.bot.send_message(
                chat_id=chat_id,
                text=name+"\nФильм Joker\n20$"
           )
        elif data.split("_")[1] == "2":
            context.bot.send_message(
               chat_id=chat_id,
               text=name+"\nФильм The Godfather\n10$"
           )
 
def main():
    updater = Updater(token=TOKEN, use_context=True)
    start_handler = CommandHandler("start", start)
    message_handler = MessageHandler(Filters.text, echo)
    button_handler = CallbackQueryHandler(
        callback=keyboard_callback_handler, 
        pass_chat_data=True
    )
 
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(button_handler)
 
    updater.start_polling()
 
 
if __name__ == '__main__':
    main()