#!/bin/bash

#Test Flask App  

#Default response 
#docker-compose exec mids curl http://localhost:5000/

#Return Prices of all Assets
#docker-compose exec mids curl http://localhost:5000/return_price

#Return price of specific asset - i.e. stock_a
#docker-compose exec mids curl http://localhost:5000/return_asset_price/stock_a

#Create new user- i.e. Tim Peters and Preethi Raju
#docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "tpeters", "full_name": "Tim Peters"}' http://localhost:5000/open_account/
#docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "praju", "full_name": "Preethi Raju"}' http://localhost:5000/open_account/

#Return information on account
#docker-compose exec mids curl http://localhost:5000/return_account_info/tpeters

#Delete account 
#docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "praju", "full_name": "Preethi Raju"}' http://localhost:5000/delete_account/

#Deposit Amount
#docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "tpeters", "amount": "200"}' http://localhost:5000/deposit/

#Withdraw Amount
#docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "tpeters", "amount": "10"}' http://localhost:5000/withdraw/

#Buy Asset
#docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "tpeters", "number_of": "10", "asset_name": "stock_a"}' http://localhost:5000/buy_asset/

#Sell Asset 
#docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "tpeters", "number_of": "2", "asset_name": "stock_a"}' http://localhost:5000/sell_asset/

#Apache Bench - test 1 
#while true; do docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "tpeters", "full_name": "Tim Peters"}' http://localhost:5000/open_account/; sleep 1; done

#docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/create_account.txt -T application/json http://localhost:5000/open_account/






