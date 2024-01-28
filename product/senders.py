from telebot import types
from api import get_packs, get_products
from shared.buttons import back_btn
from shared.messages import waiting_message, products_msg, packs_msg
from bot import bot
import json
from state import product_state


def product_list(message):
    try:
        resposne = get_products(message.from_user.id)
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
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
        bot.send_message(message.chat.id, products_msg, reply_markup=markup)
    except:
        bot.send_message(message.chat.id, waiting_message)



def pack_list(message):
    try:
        pack_id = product_state.selected_product["id"]
        resposne = get_packs(pack_id, message.from_user.id)
        markup = types.InlineKeyboardMarkup(row_width=8)
        markup.add(
            types.InlineKeyboardButton("السعر", callback_data="hey2"),
            types.InlineKeyboardButton("الاسم", callback_data="hey1"),
            types.InlineKeyboardButton("التوفر", callback_data="hey"),
            )
        for pack in resposne:
            data = f"order_details+{pack['id']}" 
            markup.add(
                types.InlineKeyboardButton(f'{pack["price"]} نقطة', callback_data=data),
                types.InlineKeyboardButton(text=pack["name"], callback_data=data),
                types.InlineKeyboardButton(pack["count"], callback_data=data),
                )
        markup.add(
            types.InlineKeyboardButton(text="رجوع", callback_data="product_list"),
        )
        markup = markup
        bot.send_message(message.chat.id, packs_msg, reply_markup=markup)
    except:
        bot.send_message(message.chat.id, waiting_message)