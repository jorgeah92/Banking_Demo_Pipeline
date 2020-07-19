
@app.route("/delete_account")
def delete_account():
    delete_account_event = {'event_type': 'delete_account',
                            'description': 'Deleting account!'}
    log_to_kafka('events', delete_account_event)
    return "Account Deleted!\n"


#buy or sell asset 
@app.route("/buy_asset", methods = ['POST'])
def make_a_depoist():
    buy_asset_event = {'event_type': 'buy_asset'}
    log_to_kafka('events', buy_asset_event)
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

