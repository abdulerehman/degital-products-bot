import telebot
from telebot import types
import requests
import json


KEY = "6852207591:AAH9CEoxLGFmo_OhwXK2ai-rgPHPEvXqYrw"
API = "http://127.0.0.1:8000/"
headers = {'Content-Type': 'application/json'}

waiting_message = " لقد استقبلنا طلبك سوف يتم اضافتك في البوت في دقائق قليله من طرف الادمن شكرا على انتظارك 🥰"
signup_button = 'سجل نفسك 📋'
cancel_button = 'الغاء'
full_name_message = 'الرجاء أكتب الإسم و اللقب الخاص بك'
phone_number_message = 'الرجاء أكتب رقم الهاتف الخاص بك'

welcome_message = "مرحبا بك عزيزي التاجر في البوت رقم واحد في البيع بالجملة كل من الاشتراكات والمنتوجات التي لها علاقة بالڨايمينڨ ( Xbox - Psn - Pc) 😍" 
welcome_message_2 = "• اهلأ بك عزيزي التاجر {name} 👋🏼 .\nنحن هنا لنوفر لكم كل منتجات جملة بأفضل اسعار 🤩\nمعلوماتك {pk}\nنقاطك   {balance}\n• قم بأختيار القسم الذي تريده من الاسفل 👇🏽."

balance_btn = "💰 رصيدي"
products_btn = "🛒 العروض التي يقدمها البوت"
ask_for_balance_btn = "💵 شحن حسابي "
contact_us_btn = "☎️ تواصل معنا"
history_btn = "📋 تعاملاتي"
buy_btn = "شراء"

history_msg = """
🌀 مرحباً بك في قسم معلومات حسابك ببوت المتجر! 🌀

رصيد حسابك الحالي: {balance} نقطة

إحصائيات حسابك:
- 🛒 السلع التي اشتريتها: {orders}
- 💸 الرصيد الذي استخدمته: {used_balance}
\n
"""
balance_msg = """
🌀 مرحباً بك في قسم معلومات رصيدي ببوت المتجر! 🌀

رصيد حسابك الحالي: {balance} نقطة
\n
""" 
contact_us_msg = """
تريد ايداع شكوى او استفسار امر ما تواصل معنا من هنا : 
☎️ رقم الهاتف 0794909201
واتساب 213794909201+
تيليڨرام Skilled04@
"""

products_msg = """
اختر عرض من هذه العروض
"""

packs_msg="""
اختر المنتوج الذي تريد شراؤه
"""

buy_msg = """
🔖 اسم السلعة: {pack}
📝 وصف السلعة: {description}

💲 السعر الحالي: {price} نقطة
✅ حالة التوفر: {count}

❓ - هل أنت متأكد من رغبتك في الشراء؟
"""

success_msg = """
🎉 عملية شراء ناجحة! 🎉

💸 تم خصم {price} نقطة بنجاح!

🎁 السلعة التي اخترتها هي:
 
{code}
"""

error_msg = "رصيدك غير كاف"

bot = telebot.TeleBot(KEY, parse_mode=None)

class ProductsState:
    def __init__(self) -> None:
        self.products = []
        self.selected_product = None

    def clear(self):
        self.products = []
        self.selected_product = None
    
    def add(self, product):
        self.products.append(product)
    
    def get(self):
        return self.products

    def check(self, title):
        for product in self.products:
            if title == product['title']:
                self.selected_product = product 
                return True
        return False


class PackState:
    def __init__(self) -> None:
        self.packs = []
        self.selected_pack = None

    def clear(self):
        self.packs = []
        self.selected_pack = None

    
    def add(self, pack):
        self.packs.append(pack)
    
    def get(self):
        return self.packs

    def check(self, title):
        for pack in self.packs:
            if title == pack['title']:
                self.selected_pack = pack 
                return True
        return False



product_state = ProductsState()
pack_state = PackState()

def signup(data):
    response = requests.post(API+"user/create", data=stringify(data), headers=headers)
    return response.json()

def get_details(id):
    response = requests.get(API + f"user/details/{id}")
    return response.json()


def get_products():
    response = requests.get(API + f"products/list")
    return response.json()

def get_order_details(id):
    response = requests.get(API + f"products/order/details/{id}")
    return response.json()


def get_packs(id):
    response = requests.get(API + f"products/pack/{id}")
    return response.json()

def buy(data):
    response = requests.post(API + f"products/buy", data=stringify(data))
    return response.json()


def stringify(data):
    return json.dumps(data)

def loads(data):
    return json.loads(data)

@bot.message_handler(func=lambda message: message.text.lower() == cancel_button)
@bot.message_handler(commands=['start'])
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
                pk=response.get('pk'),
                name=response.get('full_name'),
                balance=response.get('balance')
                ), 
            reply_markup=markup)
    
    if response.get('active') == None :
        itembtn1 = types.InlineKeyboardButton(signup_button)
        markup.add(itembtn1)
        bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

# Sign Up steps

@bot.message_handler(func=lambda message: message.text.lower() == signup_button)
def get_full_name(message):

    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.InlineKeyboardButton(cancel_button)
    markup.add(itembtn1)

    user_id = message.from_user.id
    username = message.from_user.username
    bot.send_message(message.chat.id, full_name_message, reply_markup=markup)
    bot.register_next_step_handler(message,get_phone_number, data={"tg_username": username, "tg_id":user_id})


def get_phone_number(message, data):
    data['full_name'] = message.text
    bot.send_message(message.chat.id, phone_number_message)
    bot.register_next_step_handler(message, send_waiting_message, data=data)


def send_waiting_message(message, data):
    data['phone_number'] = message.text
    signup(data)
    bot.send_message(message.chat.id, waiting_message)

# End Signup Steps

ask_for_balance_btn

@bot.message_handler(func=lambda message: message.text.lower() == balance_btn)
def get_full_name(message):
    response = get_details(message.from_user.id)
    bot.send_message(message.chat.id, balance_msg.format(balance=response.get('balance')))


@bot.message_handler(func=lambda message: message.text.lower() == history_btn)
def get_full_name(message):
    response = get_details(message.from_user.id)
    bot.send_message(message.chat.id, history_msg.format(balance=response.get('balance'), orders=response.get('orders'), used_balance=response.get('used_balance')))

@bot.message_handler(func=lambda message: message.text.lower() == contact_us_btn)
def get_full_name(message):
    bot.send_message(message.chat.id, contact_us_msg)



@bot.message_handler(func=lambda message: message.text.lower() == products_btn)
def product_list(message):
    
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
    
    bot.send_message(message.chat.id, products_msg, reply_markup=markup)



@bot.message_handler(func=lambda message: product_state.check(message.text))
def pack_list(message):
    
    pack_id = product_state.selected_product["id"]
    resposne = get_packs(pack_id)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    resposne = json.loads(resposne)
    arr = []
    pack_state.clear()

    for pack in resposne:
        if len(arr) == 0:
            arr.append(types.InlineKeyboardButton(pack['fields']["name"]))
        elif len(arr) == 1:
            arr.append(types.InlineKeyboardButton(pack['fields']["name"]))
            markup.add(arr[0], arr[1])
            arr = []
        pack_state.add({"title":pack['fields']["name"], "id": pack['pk']})

    if len(arr) == 1:
        markup.add(types.InlineKeyboardButton(pack['fields']["name"]))
    
    bot.send_message(message.chat.id, packs_msg, reply_markup=markup)


#pack_id = product_state.selected_product["id"]
#tg_id = message.from_user.id

@bot.message_handler(func=lambda message: pack_state.check(message.text))
def order_details(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    resposne = get_order_details(pack_state.selected_pack["id"])
    btns = [
        types.InlineKeyboardButton(cancel_button),
        types.InlineKeyboardButton(buy_btn),
    ]

    if resposne["count"] == 0:
        markup.add(btns[0])
    else:
        markup.add(btns[0], btns[1])

    reply = buy_msg.format(
        pack=resposne["title"], 
        description=resposne["description"],
        count=resposne["count"],
        price=resposne["price"]
    )
    bot.send_message(message.chat.id, reply, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == buy_btn)
def get_code(message):
    user_id = message.from_user.id
    resposne = buy({
        "pack_id":pack_state.selected_pack["id"],
        "tg_id": user_id
    })
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(cancel_button))
    try:
        bot.send_message(message.chat.id, success_msg.format(
            code=resposne["code"],
            price=resposne["price"]
        ), reply_markup=markup)
    except KeyError:
        bot.send_message(message.chat.id, error_msg, reply_markup=markup)



print("--------- Bot is Running 📋 --------")
bot.infinity_polling()