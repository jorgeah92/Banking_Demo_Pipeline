#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request, jsonify, make_response
from datetime import datetime, date 
import math 


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
        if asset_type == 'stock': 
            r = 0.1
        elif asset_type == 'bond': 
            r = 0.04
        elif asset_type == 'cash': 
            r = 0 
        else: 
            return 'Please enter correct asset type.'
        new_value = original_price * math.exp(r * (float(delta) / 365))
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
        index_value = accounts.index(original_account)
        accounts[index_value] = new_account
        return new_account
    


##### SCHEMAS #####

class Schema: 
    
    def __init__(self, json_data):  
        self.json_data = json_data  
    
    def validate_account_schema(self): 
        required_keys = ['full_name', 'user_id']
        if all(elem in self.json_data for elem in required_keys): 
            return True 

    def validate_deposit_schema(self): 
        required_keys = ['amount', 'user_id']
        if all(elem in self.json_data for elem in required_keys): 
            try: 
                float(self.json_data['amount'])
                return True 
            except: 
                return False

    def validate_asset_schema(self): 
        required_keys = ['number_of', 'user_id', 'asset_name']
        if all(elem in self.json_data for elem in required_keys): 
            try: 
                int(self.json_data['number_of'])
                return True 
            except: 
                return False            
        
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
@app.route("/return_price", methods = ['GET'])
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
    asset_info = [i for i in assets if i['asset_name'] == asset_name]
    if len(asset_info) == 0:
        abort(404)
    return jsonify(asset_info[0])

@app.route('/return_account_info/<user_id>', methods=['GET'])
def get_account_info(user_id):
    if user_id in [i['user_id'] for i in accounts]: 
        return_account_event = {'event_type': 'return_account_information',
                                'description': 'return account into for ' + user_id}
        log_to_kafka('events', return_account_event)
        return jsonify(AssetValue().update_account_value(user_id))
    else: 
        return jsonify({"message": "User ID not found"}), 400

#open or delete an account
@app.route("/open_account/", methods=["POST"])
def open_account():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    elif not Schema(json_data).validate_account_schema(): 
        return jsonify({"message": "Must provide user_name and user_id."}), 400
    elif json_data['user_id'] in [i['user_id'] for i in accounts]: 
        return "Account already exists! Pick a unique username.\n"
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
        return jsonify({"message": "No input data provided"}), 400
    elif not Schema(json_data).validate_account_schema(): 
        return jsonify({"message": "Must provide user_name and user_id."}), 400
    elif json_data['full_name'] not in [i['full_name'] for i in accounts]: 
        return jsonify({"message": "Must provide existing user_name and user_id."}), 400
    else: 
        remove_value = [i for i in accounts if i['full_name'] == json_data['full_name']][0]
        accounts.remove(remove_value)
        delete_account_event = {'event_type': 'delete_account',
                                'description': 'Deleting account'}
        log_to_kafka('events', delete_account_event)
        return "Account Deleted!\n"


#Withdraw or deposit money 
@app.route("/deposit/", methods = ['POST'])
def make_a_deposit():
    
    def log_deposit(user_id): 
        make_deposit_event = {'event_type': 'make_deposit'}
        log_to_kafka('events', make_deposit_event)
        AssetValue().update_account_value(user_id)
        return "Amount deposited!\n"
    
    json_data = request.get_json()
    print(Schema(json_data).validate_deposit_schema())
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    elif not Schema(json_data).validate_deposit_schema(): 
        return jsonify({"message": "Must provide valid user_id and amount."}), 400
    elif json_data['user_id'] not in [i['user_id'] for i in accounts]: 
        return "Account doesn't exist!\n"
    else: 
        add_cash = float(json_data['amount'])
        for n, i in enumerate(accounts): 
            if i['user_id'] == json_data['user_id']: 
                if 'transactions' in i and 'cash' in [s['asset_type'] for s in i['transactions']]: 
                    for k in i['transactions']: 
                        if k['asset_type'] == 'cash': 
                            k['number_of']+= add_cash
                            k['original_value']+= add_cash
                            k['current_value']+= add_cash
                            k['transaction_date'] = datetime.today().strftime("%Y-%m-%d")
                            return log_deposit(json_data['user_id'])
                else: 
                    i.append({'asset_name': 'cash',
                              'asset_type' : 'cash',
                              'number_of' : add_cash,
                              'original_value' : add_cash,
                              'transaction_date': datetime.today().strftime("%Y-%m-%d"),
                              'current_value' : add_cash
                             })
                    return log_deposit(json_data['user_id'])



@app.route("/withdraw/", methods = ['POST'])
def make_a_withdrawal():
    
    def log_withdrawal(user_id): 
        make_withdrawal_event = {'event_type': 'make_withdrawal'}
        log_to_kafka('events', make_withdrawal_event)
        AssetValue().update_account_value(user_id)
        return "Amount withdrawn!\n"
    
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    elif not Schema(json_data).validate_deposit_schema(): 
        return jsonify({"message": "Must provide valid user_id and amount."}), 400
    elif json_data['user_id'] not in [i['user_id'] for i in accounts]: 
        return "Account doesn't exist!\n"
    else: 
        withdraw_cash = float(json_data['amount'])
        for i in accounts: 
            if i['user_id'] == json_data['user_id']: 
                if 'transactions' in i and 'cash' in [s['asset_type'] for s in i['transactions']]: 
                    for k in i['transactions']: 
                        if k['asset_type'] == 'cash': 
                            if k['current_value'] >= withdraw_cash: 
                                k['number_of']-= withdraw_cash
                                k['original_value']-= withdraw_cash
                                k['current_value']-= withdraw_cash
                                k['transaction_date'] = datetime.today().strftime("%Y-%m-%d")
                                return log_withdrawal(json_data['user_id'])
                        else: 
                            return 'Overdraft! Too much money withdrawn. The transaction will be cancelled.\n'
                else: 
                    return 'Please deposit cash in your account before withdrawing.\n'


                
#buy or sell asset 
@app.route("/buy_asset/", methods = ['POST'])
def buy_an_asset():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    elif not Schema(json_data).validate_asset_schema(): 
        return jsonify({"message": "Must provide valid user_id and amount; make sure account has cash."}), 400
    elif json_data['user_id'] not in [i['user_id'] for i in accounts]: 
        return "Account doesn't exist!\n"
    else: 
        AssetValue().update_asset_price()
        for n, m in enumerate(accounts): 
            if m['user_id'] == json_data['user_id']: 
                for c, i in enumerate(m['transactions']): 
                    if i['asset_type'] == 'cash': 
                        cash_value = i['current_value']
                        asset_price = [s['price'] for s in assets if s['asset_name'] == json_data['asset_name']][0]
                        asset_number_of = int(json_data['number_of'])
                        asset_total_value =  round(asset_price * asset_number_of,2)
                        if cash_value >= asset_total_value: 
                            cash_left  = round(i['current_value'] - asset_total_value, 2)
                            i['current_value'], i['original_value'], i['number_of']  = cash_left, cash_left, cash_left
                            m['transactions'].append({
                                'asset_name': json_data['asset_name'],
                                'asset_type' : [i['asset_type'] for i in assets if i['asset_name'] == json_data['asset_name']][0],
                                'number_of' : asset_number_of,
                                'original_value' : asset_total_value,
                                'transaction_date': datetime.today().strftime("%Y-%m-%d"),
                                'current_value' : asset_total_value
                            })
                            buy_asset_event = {'event_type': 'buy_asset'}
                            log_to_kafka('events', buy_asset_event)
                            AssetValue().update_account_value(json_data['user_id'])
                            return 'Asset purchased!\n'
                        else: 
                            return 'Not enough money to purchase asset!\n'

                        
@app.route("/sell_asset/", methods = ['POST'])
def sell_an_asset():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    elif not Schema(json_data).validate_asset_schema(): 
        return jsonify({"message": "Must provide valid user_id and amount; make sure account has cash."}), 400
    elif json_data['user_id'] not in [i['user_id'] for i in accounts]: 
        return "Account doesn't exist!\n"
    elif json_data['asset_name'] not in [i['asset_name'] for i in assets]: 
        return "Asset doesn't exist!\n"
    else: 
        AssetValue().update_asset_price()
        AssetValue().update_account_value(json_data['user_id'])
        number_of = int(json_data['number_of'])
        for n, m in enumerate(accounts): 
            if m['user_id'] == json_data['user_id']: 
                combine_asset = {
                    'asset_name': json_data['asset_name'],
                    'asset_type' : [i['asset_type'] for i in assets if i['asset_name'] == json_data['asset_name']][0], 
                    'number_of' : 0,
                    'original_value' : 0,
                    'transaction_date': datetime.today().strftime("%Y-%m-%d"), 
                    'current_value' : 0
                }
                for c, i in enumerate(m['transactions']): 
                    if i['asset_name'] == json_data['asset_name']:
                        combine_asset['number_of'] += i['number_of']
                        combine_asset['original_value'] += i['original_value']
                        combine_asset['current_value'] += i['current_value']
                        m['transactions'].remove(i)
                if combine_asset['number_of'] < number_of: 
                    return "You don\'t known enough of the asset!"
                else: 
                    combine_asset['original_value'] -= (number_of * combine_asset['original_value'] / combine_asset['number_of'])
                    new_current_value = round((number_of * combine_asset['current_value'] / combine_asset['number_of']),2)
                    combine_asset['current_value'] -= new_current_value
                    combine_asset['number_of'] -= number_of
                for c, i in enumerate(m['transactions']): 
                    if i['asset_name'] == 'cash': 
                        i['current_value'] += new_current_value
                        i['original_value'] += new_current_value
                        i['number_of'] += new_current_value
                m['transactions'].append(combine_asset)
                sell_asset_event = {'event_type': 'sell_asset'}
                log_to_kafka('events', sell_asset_event)
                return 'Asset sold!\n'


                