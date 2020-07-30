#!/bin/bash

pip install docker-compose
docker-compose up -d

#docker-compose logs -f kafka

#Create topic events
 docker-compose exec kafka \
   kafka-topics \
     --create \
     --topic events \
     --partitions 1 \
     --replication-factor 1 \
     --if-not-exists \
     --zookeeper zookeeper:32181
     
#Run Flask 
docker-compose exec mids \
  env FLASK_APP=/w205/Project-3-w205-JHR/banking_game_api.py \
  flask run --host 0.0.0.0
  
#CHANGE ENVIRONMENT PATH WHEN TURNING IN PROJECT ?? 
  
#Test Flask app   

#pip install httpie

#docker-compose exec mids curl http://localhost:5000/
#docker-compose exec mids curl http://localhost:5000/return_price
#docker-compose exec mids curl http://localhost:5000/return_asset_price/stock_a
#docker-compose exec mids curl http://localhost:5000/return_account_info/praju

#http POST :5000/open_account/ full_name="Tim Peters" user_id="tpeters"
#http POST :5000/delete_account/ full_name="Tim Peters" user_id="tpeters"

#http POST :5000/deposit/ user_id="praju" amount=200
#http POST :5000/withdraw/ user_id="praju" amount=50

#http POST :5000/buy_asset/ user_id="praju" number_of=2 asset_name=stock_a
#http POST :5000/sell_asset/ user_id="praju" number_of=2 asset_name=stock_a


#Kafka
#docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning

#Apache Bench


#docker-compose down 

