import requests
import json
from config import API, API_TOKEN

headers = {'Content-Type': 'application/json', "Authorizations": API_TOKEN}


def stringify(data):
    return json.dumps(data)

def loads(data):
    return json.loads(data)

def signup(data):
    response = requests.post(API+"user/create", data=stringify(data), headers=headers)
    return response.json()

def get_details(id):
    response = requests.get(API + f"user/details/{id}", headers=headers)
    return response.json()


def get_products(user_id):
    headers["User"] = str(user_id)
    response = requests.get(API + f"products/list", headers=headers)
    return response.json()

def get_order_details(id,user_id):
    headers["User"] = str(user_id)
    response = requests.get(API + f"products/order/details/{id}", headers=headers)
    return response.json()


def get_packs(id, user_id):
    headers["User"] = str(user_id)
    response = requests.get(API + f"products/pack/{id}", headers=headers)
    return response.json()

def buy(data, user_id):
    headers["User"] = str(user_id)
    response = requests.post(API + f"products/buy", data=stringify(data), headers=headers)
    return response.json()
