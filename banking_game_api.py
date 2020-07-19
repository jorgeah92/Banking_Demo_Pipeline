#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request, jsonify, make_response
from datetime import date 
import math


app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


assets = [
    {
        'name': 'stock_a',
        'asset_type' : 'stock', 
        'price': 20
    },
    {
        'name': 'bond_a',
        'asset_type' : 'bond', 
        'price': 10
    }
]


accounts = [
    {
        'full_name': 'Preethi Raju', 
        'user_id': 'praju', 
        'asset_type': 'cash', 
        'value' : 100, 
        'date': '2020-07-18'
    }
]


##### SCHEMAS #####


##### LOGGING #####

def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())
    
    
##### CUSTOM ERROR HANDLING #####

#@app.errorhandler(404)
#def not_found(error):
#    return make_response(jsonify({'Error': 'Not found'}), 404)


@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "Welcome to your W205 investing account!\n"

#return price of assets 
@app.route("/return_price", methods = ['GET'])
def return_price():
    return_price_event = {'event_type': 'return_price'}
    log_to_kafka('events', return_price_event)
    return jsonify(assets)

@app.route('/return_price/<asset_name>', methods=['GET'])
def get_task(asset_name):
    asset_price_event = {'event_type': 'get_asset_price',
                         'description': 'Get price for ' + asset_name}
    log_to_kafka('events', asset_price_event)
    asset_info = [i for i in assets if i['name'] == asset_name]
    if len(asset_info) == 0:
        abort(404)
    return jsonify(asset_info[0])


#open or delete an account
@app.route("/open_account/", methods=["POST"])
def open_account():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    else: 
        print(json_data['author'])
    #Check if account exists 
    #If account doesn't exist, add it to list 
    open_account_event = {'event_type': 'open_account',
                          'description': 'Opening account'}
    log_to_kafka('events', open_account_event)
    return "Account Opened!\n"



#PUT to modify account value once account is created 