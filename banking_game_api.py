#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request, jsonify, make_response
from datetime import datetime, date 


app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


assets = [
    {
        'asset_name': 'stock_a',
        'asset_type' : 'stock', 
        'price': 5, 
        'as_of' : '2020-01-01'
    },
    {
        'asset_name': 'bond_a',
        'asset_type' : 'bond', 
        'price': 5, 
        'as_of' : '2020-01-01'
    }, 
    {
        'asset_name': 'cash',
        'asset_type' : 'cash', 
        'price': 1, 
        'as_of' : '2020-01-01'
    }
]

accounts = [
    {
        'full_name': 'Preethi Raju', 
        'user_id': 'praju', 
        'total_value': 200, 
        'original_value' : 200, 
        'as_of' : '2020-07-18', 
        'transactions' : 
        [
            {
                'asset_name': 'cash',
                'asset_type' : 'cash', 
                'number_of' : 100,
                'original_value' : 100,
                'transaction_date': '2020-01-01', 
                'current_value' : 100
            }, 
            {
                'asset_name': 'stock_a',
                'asset_type' : 'stock', 
                'number_of' : 20,
                'original_value' : 100,
                'transaction_date': '2020-01-01', 
                'current_value' : 100
            }
        ]
    }
]

##### HELPER FUNCTIONS #####

class AssetValue: 
    
    def __init__(self): 
        self.today = datetime.today() 
        self.today_str = self.today.strftime("%Y-%m-%d")
    
    def asset_new_value(self, asset_name, asset_type, original_date, original_price):
        t = self.today - datetime.strptime(original_date, '%Y-%m-%d')
        delta = t.days
        print(delta)
        if asset_type == 'stock': 
            r = 0.1
        elif asset_type == 'bond': 
            r = 0.04
        elif asset_type == 'cash': 
            r = 0 
        else: 
            return 'Please enter correct asset type.'
        new_value = original_price * 2.718281828459045**(r * (delta / 365))
        print(new_value)
        return new_value  
    
    def update_asset_price(self): 
        if assets[0]['as_of']!= self.today_str: 
            print('updating asset values')
            for n, i in enumerate(assets): 
                original = i 
                new = original.copy()
                new['price']  = self.asset_new_value(original['asset_name'], 
                                                     original['asset_type'], 
                                                     original['as_of'], 
                                                     original['price'])
                new['as_of'] = self.today_str
                assets[n] = new 
        return 'Asset value updated' 
    
    def update_account_value(self, user_id): 
        self.update_asset_price()
        original_account = [i for i in accounts if user_id == i['user_id']][0]
        new_account = original_account.copy()
        for i in new_account['transactions']: 
            asset_value = [a for a in assets if i['asset_name'] == a['asset_name']][0]['price']
            i['current_value'] = round(i['number_of'] * asset_value,2)
        new_account['as_of'] = self.today_str
        new_account['original_value'] = round(sum([i['original_value'] for i in new_account['transactions']]),2)
        new_account['total_value'] = round(sum([i['current_value'] for i in new_account['transactions']]),2)
        print(new_account)
        accounts[accounts.index(original_account)] = new_account
        return new_account
    


##### SCHEMAS #####

class Schema: 
    
    def __init__(self, json_data):  
        self.json_data = json_data  
    
    def validate_account_schema(self): 
        required_keys = ['full_name', 'user_id']
        if all(elem in self.json_data for elem in required_keys): 
            return True 


##### LOGGING #####

def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())
    
##### ROUTING #####

@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "Welcome to your W205 investing account!\n"

#return price of assets or account information 
@app.route("/return_asset_price", methods = ['GET'])
def return_price():
    return_price_event = {'event_type': 'return_asset_price', 
                         'description': 'Return price for all assets'}
    log_to_kafka('events', return_price_event)
    return jsonify(assets)

@app.route('/return_asset_price/<asset_name>', methods=['GET'])
def get_asset_price(asset_name):
    asset_price_event = {'event_type': 'return_asset_price',
                         'description': asset_name}
    log_to_kafka('events', asset_price_event)
    asset_info = [i for i in assets if i['name'] == asset_name]
    if len(asset_info) == 0:
        abort(404)
    return jsonify(asset_info[0])

@app.route('/return_account_info/<user_id>', methods=['GET'])
def get_account_info(user_id):
    print(user_id)
    if user_id in [i['user_id'] for i in accounts]: 
        return_account_event = {'event_type': 'return_account_information',
                                'description': 'return account into for ' + user_id}
        log_to_kafka('events', return_account_event)
        new_account = AssetValue().update_account_value(user_id)
        return new_account
    else: 
        return {"message": "User ID not found"}, 400

#open or delete an account
@app.route("/open_account/", methods=["POST"])
def open_account():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    elif not Schema(json_data).validate_account_schema(): 
        return {"message": "Must provide user_name and user_id."}, 400
    elif json_data['full_name'] in [i['full_name'] for i in accounts]: 
        return "Account already exists!\n"
    else: 
        accounts.append({
            'full_name': json_data['full_name'], 
            'user_id': json_data['user_id'],
            'total_value': 0, 
            'original_value': 0, 
            'as_of' : str(date.today())
        })
        open_account_event = {'event_type': 'open_account',
                              'description': 'Opening account'}
        log_to_kafka('events', open_account_event)
        return "Account Opened!\n"

    
@app.route("/delete_account/", methods=["POST"])
def delete_account():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    elif not Schema(json_data).validate_account_schema(): 
        return {"message": "Must provide user_name and user_id."}, 400
    elif json_data['full_name'] not in [i['full_name'] for i in accounts]: 
        return {"message": "Must provide existing user_name and user_id."}, 400
    else: 
        remove_value = [i for i in accounts if i['full_name'] == json_data['full_name']][0]
        accounts.remove(remove_value)
        delete_account_event = {'event_type': 'delete_account',
                                'description': 'Deleting account'}
        log_to_kafka('events', delete_account_event)
        return "Account Deleted!\n"

