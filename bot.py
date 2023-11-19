import telebot
from telebot import types
import requests
import json

ADMIN_CHAT_ID = "1045530860"
KEY = "6852207591:AAH9CEoxLGFmo_OhwXK2ai-rgPHPEvXqYrw"
API = "http://127.0.0.1:8000/"
headers = {'Content-Type': 'application/json', "Authorizations":"ttg45"}

waiting_message = " لقد استقبلنا طلبك سوف يتم اضافتك في البوت في دقائق قليله من طرف الادمن شكرا على انتظارك 🥰"
signup_button = 'سجل نفسك 📋'
cancel_button = 'الغاء'
full_name_message = 'الرجاء أكتب الإسم و اللقب الخاص بك'
phone_number_message = 'الرجاء أكتب رقم الهاتف الخاص بك'

welcome_message = "مرحبا بك عزيزي التاجر في البوت رقم واحد في البيع بالجملة كل من الاشتراكات والمنتوجات التي لها علاقة بالڨايمينڨ ( Xbox - Psn - Pc) 😍" 
welcome_message_2 = "• اهلأ بك عزيزي التاجر {name} 👋🏼 .\nنحن هنا لنوفر لكم كل منتجات جملة بأفضل اسعار 🤩\nمعلوماتك {pk}\nنقاطك   {balance}\n• قم بأختيار القسم الذي تريده من الاسفل 👇🏽."

balance_btn = "💰 رصيدي"
products_btn = "🛒 العروض التي يقدمها البوت"
ask_for_balance_btn = "💵 شحن حسابي"
contact_us_btn = "☎️ تواصل معنا"
history_btn = "📋 تعاملاتي"
buy_btn = "شراء"
back_btn = "رجوع"

admin_msg = """
الزبون: {user} 
إشترى المنتوج: {pack} 
بسعر : {price}
الآن
"""
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

ask_for_balance_msg = """
تريد شحن حسابك لشراء منتجاتنا تواصلوا معنا هنا: 
☎️ رقم الهاتف 0794909201
📱واتساب 213794909201+
✉️ تيليڨرام Skilled04@
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
    response = requests.get(API + f"user/details/{id}", headers=headers)
    return response.json()


def get_products():
    response = requests.get(API + f"products/list", headers=headers)
    return response.json()

def get_order_details(id):
    response = requests.get(API + f"products/order/details/{id}", headers=headers)
    return response.json()


def get_packs(id):
    response = requests.get(API + f"products/pack/{id}", headers=headers)
    return response.json()

def buy(data):
    response = requests.post(API + f"products/buy", data=stringify(data), headers=headers)
    return response.json()


def stringify(data):
    return json.dumps(data)

def loads(data):
    return json.loads(data)

@bot.message_handler(func=lambda message: message.text.lower() == cancel_button)
@bot.message_handler(func=lambda message: message.text.lower() == back_btn)
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

@bot.message_handler(func=lambda message: message.text.lower() == signup_button)
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

# End Signup Steps


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



@bot.message_handler(func=lambda message: product_state.check(message.text))
def pack_list(message):
    pack_id = product_state.selected_product["id"]
    resposne = get_packs(pack_id)
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton(text="السعر", callback_data="hey2"),
        types.InlineKeyboardButton(text="الاسم", callback_data="hey1"),
        types.InlineKeyboardButton(text="التوفر", callback_data="hey"),
        )
    for pack in resposne:
        data = f"order_details+{pack['id']}" 
        markup.add(
            types.InlineKeyboardButton(text=pack["price"], callback_data=data),
            types.InlineKeyboardButton(text=pack["name"], callback_data=data),
            types.InlineKeyboardButton(text=pack["count"], callback_data=data),
            )
    markup.add(
        types.InlineKeyboardButton(text="رجوع", callback_data="product_list"),
    )
    markup = markup
    bot.send_message(message.chat.id, packs_msg, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    func = call.data.split("+")[0]
    if func == 'order_details':
        id = call.data.split("+")[1]
        order_details(call.message, id)
        return
    elif func == "product_list":
        pack_state.selected_pack = None
        product_list(call.message)


def order_details(message, id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    resposne = get_order_details(id)
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


@bot.message_handler(func=lambda message: message.text == buy_btn)
def get_code(message):
    user_id = message.from_user.id
    resposne = buy({
        "pack_id":pack_state.selected_pack,
        "tg_id": user_id
    })
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
            code=resposne["code"],
            price=resposne["price"]
        ), reply_markup=markup)
        bot.send_message(ADMIN_CHAT_ID, admin_msg.format(
            pack=resposne["pack"],
            user=resposne["user"],
            price=resposne["price"]
        ))
    except KeyError:
        bot.send_message(message.chat.id, error_msg, reply_markup=markup)
    product_list(message, False)

@bot.message_handler(func=lambda message: message.text == ask_for_balance_btn)
def ask_for_balance(message):
    bot.send_message(message.chat.id, ask_for_balance_msg)


print("--------- Bot is Running 📋 --------")
bot.infinity_polling()