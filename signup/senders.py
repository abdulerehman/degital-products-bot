from telebot import types
from bot import bot
from api import get_details, signup
from shared.buttons import (
    balance_btn,
    products_btn,
    ask_for_balance_btn,
    contact_us_btn,
    history_btn,
    signup_button,
    cancel_button
)
from shared.messages import (
    waiting_message, 
    welcome_message_2, 
    full_name_message, 
    phone_number_message,
    welcome_message,
    ) 



def send_welcome(message):
    response = get_details(message.from_user.id)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    if response.get('active') == False :
        bot.send_message(message.chat.id, waiting_message)
    if response.get('active') == True :
        markup.add(
            types.InlineKeyboardButton(balance_btn),
            types.InlineKeyboardButton(products_btn)
        )
        markup.add(
            types.InlineKeyboardButton(ask_for_balance_btn),
            types.InlineKeyboardButton(contact_us_btn),
        )
        markup.add(
            types.InlineKeyboardButton(history_btn)
        )
        bot.send_message(
            message.chat.id, 
            welcome_message_2.format(
                pk=message.from_user.id,
                name=response.get('full_name'),
                balance=response.get('balance')
                ), 
            reply_markup=markup)
    
    if response.get('active') == None :
        itembtn1 = types.InlineKeyboardButton(signup_button)
        markup.add(itembtn1)
        bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

# Sign Up steps

def get_full_name(message):

    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.InlineKeyboardButton(cancel_button)
    markup.add(itembtn1)

    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id
    bot.send_message(message.chat.id, full_name_message, reply_markup=markup)
    bot.register_next_step_handler(message,get_phone_number, data={"tg_username": username, "tg_id":user_id, "chat_id": chat_id})


def get_phone_number(message, data):
    if message.text != cancel_button:
        data['full_name'] = message.text
        bot.send_message(message.chat.id, phone_number_message)
        bot.register_next_step_handler(message, send_waiting_message, data=data)


def send_waiting_message(message, data):
    if message.text != cancel_button:
        data['phone_number'] = message.text
        signup(data)
        bot.send_message(message.chat.id, waiting_message)