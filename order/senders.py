import json
from telebot import types
from api import get_order_details, get_products, buy
from product.senders import pack_list, product_list
from shared.buttons import cancel_button, buy_btn, back_btn
from shared.messages import (
    waiting_message, 
    buy_msg, 
    success_msg,
    admin_msg,
    error_msg
)
from bot import bot
from state import pack_state, product_state
from config import ADMIN_CHAT_ID



def order_details(message, id):
    try:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        resposne = get_order_details(id, message.from_user.id)
        pack_state.selected_pack = id
        btns = [
            types.InlineKeyboardButton(cancel_button),
            types.InlineKeyboardButton(buy_btn),
        ]

        if resposne["count"] == 0:
            bot.send_message(message.chat.id,"عملية شراء غير ممكنة لعدم توفر المنتوج سوف يتم تعبئته واعلامكم")
            pack_list(message)
        else:
            markup.add(btns[0], btns[1])
            reply = buy_msg.format(
                pack=resposne["title"], 
                description=resposne["description"],
                count=resposne["count"],
                price=resposne["price"]
            )
            bot.send_message(message.chat.id, reply, reply_markup=markup)
    except:
        bot.send_message(message.chat.id, waiting_message)


def get_code(message):
    try:
        user_id = message.from_user.id
        rp = buy({
            "pack_id":pack_state.selected_pack,
            "tg_id": user_id
        }, message.from_user.id)
        resposne = get_products()
        markup = types.ReplyKeyboardMarkup(row_width=2)
        resposne = json.loads(resposne)
        arr = []
        product_state.clear()
        
        for product in resposne:
            if len(arr) == 1:
                arr.append(types.InlineKeyboardButton(
                    product['fields']["title"], 
                    ))
                markup.add(arr[0], arr[1])
                arr = []
            elif len(arr) == 0:
                arr.append(types.InlineKeyboardButton(product['fields']["title"]))
            product_state.add({"title": product['fields']["title"], "id": product['pk'] })
        
        if len(arr) == 1:
            markup.add(types.InlineKeyboardButton(product['fields']["title"]))
        markup.add(
            types.InlineKeyboardButton(text=back_btn),
        )
        try:
            bot.send_message(message.chat.id, success_msg.format(
                code=rp["code"],
                price=rp["price"]
            ), reply_markup=markup)
            bot.send_message(ADMIN_CHAT_ID, admin_msg.format(
                pack=rp["pack"],
                user=rp["user"],
                price=rp["price"]
            ))
        except :
            bot.send_message(message.chat.id, error_msg, reply_markup=markup)
        product_list(message)
    except:
        bot.send_message(message.chat.id, waiting_message)


