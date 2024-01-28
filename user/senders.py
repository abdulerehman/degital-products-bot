from bot import bot
from api import get_details
from shared.messages import balance_msg, history_msg, ask_for_balance_msg


def get_user_balance(message):
    response = get_details(message.from_user.id)
    bot.send_message(message.chat.id, balance_msg.format(balance=response.get('balance')))


def get_user_history(message):
    response = get_details(message.from_user.id)
    bot.send_message(message.chat.id, history_msg.format(balance=response.get('balance'), orders=response.get('orders'), used_balance=response.get('used_balance')))

def ask_for_balance(message):
    bot.send_message(message.chat.id, ask_for_balance_msg)