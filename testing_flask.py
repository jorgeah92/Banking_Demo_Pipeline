
#show account value

#buy or sell asset 
@app.route("/buy_asset", methods = ['POST'])
def make_a_depoist():
    buy_asset_event = {'event_type': 'buy_asset'}
    log_to_kafka('events', buy_asset_event)
    return "Asset Purchased!\n"

@app.route("/sell_asset", methods = ['POST'])
def make_a_depoist():
    sell_asset_event = {'event_type': 'make_deposit'}
    log_to_kafka('events', sell_asset_event)
    return "Asset Sold!\n"

#deposit or withdraw money 
@app.route("/withdraw", methods = ['POST'])
def make_a_depoist():
    withdraw_money_event = {'event_type': 'make_deposit'}
    log_to_kafka('events', withdraw_money_event)
    return "Amount withdraw!\n"

@app.route("/deposit", methods = ['POST'])
def make_a_depoist():
    make_deposit_event = {'event_type': 'make_deposit'}
    log_to_kafka('events', make_deposit_event)
    return "Amount deposited!\n"


#PUT to modify account value once account is created 
