#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())


@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"


@app.route("/make_a_deposit")
def make_a_depoist():
    make_deposit_event = {'event_type': 'make_deposit'}
    log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased!\n"

@app.route("/open_an_account")
def open_an_account():
    open_account_event = {'event_type': 'open_account',
                            'description': 'Welcome to nest of eggs!'}
    log_to_kafka('events', open_an_account)
    return "Account Opened!\n"
