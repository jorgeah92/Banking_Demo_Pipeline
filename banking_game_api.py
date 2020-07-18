#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request, jsonify

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


assets = [
    {
        'name': 'stock_a',
        'price': 20
    },
    {
        'name': 'bond_a',
        'price': 10
    }
]


account = [
    {
        'user_id': 1, 
        'item': 'cash', 
        'value' : 100, 
        'date': '2020-07-18'
    }
]



def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())
    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "Welcome to your W205 investing account!\n"

#return price of assets 
@app.route("/return_price", methods = ['GET'])
def make_a_depoist():
    return_price_event = {'event_type': 'return_price'}
    log_to_kafka('events', return_price_event)
    return jsonify(assets)

#buy or sell asset 
@app.route("/buy_asset", methods = ['POST'])
def make_a_depoist():
    make_deposit_event = {'event_type': 'buy_asset'}
    log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased!\n"

@app.route("/sell_asset")
def make_a_depoist():
    make_deposit_event = {'event_type': 'make_deposit'}
    log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased!\n"

#deposit or withdraw money 
@app.route("/withdraw")
def make_a_depoist():
    make_deposit_event = {'event_type': 'make_deposit'}
    log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased!\n"

@app.route("/deposit")
def make_a_depoist():
    make_deposit_event = {'event_type': 'make_deposit'}
    log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased!\n"

#open or delete an account
@app.route("/open_account")
def open_an_account():
    open_account_event = {'event_type': 'open_account',
                            'description': 'Welcome to nest of eggs!'}
    log_to_kafka('events', open_an_account)
    return "Account Opened!\n"


@app.route("/delete_account")
def open_an_account():
    open_account_event = {'event_type': 'open_account',
                            'description': 'Welcome to nest of eggs!'}
    log_to_kafka('events', open_an_account)
    return "Account Opened!\n"

