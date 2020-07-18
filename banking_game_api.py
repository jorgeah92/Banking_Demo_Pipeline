#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request, jsonify

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


account = [
    {
        'user_id': 1, 
        'asset_type': 'cash', 
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
