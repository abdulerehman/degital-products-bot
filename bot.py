import telebot
from shared.messages import contact_us_msg
from shared.buttons import contact_us_btn
from state import pack_state
from config import KEY
from shared.buttons import *
from state import product_state

bot = telebot.TeleBot(KEY, parse_mode=None)

@bot.message_handler(func=lambda message: message.text.lower() == cancel_button)
@bot.message_handler(func=lambda message: message.text.lower() == back_btn)
@bot.message_handler(commands=['start'])
def send_welcome_handler(message):
    from signup.senders import send_welcome
    send_welcome(message)

@bot.message_handler(func=lambda message: message.text.lower() == signup_button)
def get_full_name_handler(message):
    from signup.senders import get_full_name
    get_full_name(message)

@bot.message_handler(func=lambda message: message.text.lower() == products_btn)
def product_list_handler(message):
    from product.senders import product_list
    product_list(message)

@bot.message_handler(func=lambda message: product_state.check(message.text))
def pack_list_handler(message):
    from product.senders import pack_list
    pack_list(message)

@bot.message_handler(func=lambda message: message.text == buy_btn)
def get_code_handler(message):
    from order.senders import get_code
    get_code(message)

@bot.message_handler(func=lambda message: message.text.lower() == contact_us_btn)
def send_contact_us(message):
    bot.send_message(message.chat.id, contact_us_msg)


@bot.message_handler(func=lambda message: message.text.lower() == balance_btn)
def get_user_balance_handler(message):
    from user.senders import get_user_balance
    get_user_balance(message)

@bot.message_handler(func=lambda message: message.text.lower() == history_btn)
def get_user_history_handler(message):
    from user.senders import get_user_history
    get_user_history(message)

@bot.message_handler(func=lambda message: message.text == ask_for_balance_btn)
def ask_for_balance_handler(message):
    from user.senders import ask_for_balance
    ask_for_balance(message)


@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    from product.senders import product_list
    from order.senders import order_details
    func = call.data.split("+")[0]
    if func == 'order_details':
        id = call.data.split("+")[1]
        order_details(call.message, id)
        return
    elif func == "product_list":
        pack_state.selected_pack = None
        product_list(call.message)

def main():
    print("--------- Bot is Running 📋 --------")
    bot.infinity_polling()

if __name__ == "__main__":
    main()