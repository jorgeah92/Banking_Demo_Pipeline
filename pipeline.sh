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
     
#Add folder
mkdir tmp
     
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
#docker-compose exec mids curl http://localhost:5000/return_account_info/tpeters

#http POST :5000/open_account/ full_name="Tim Peters" user_id="tpeters"

docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "tpeters", "full_name": "Tim Peters"}' http://localhost:5000/open_account/

docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "tpeters", "full_name": "Tim Peters"}' http://localhost:5000/delete_account/


ab -p post_loc.txt -T application/json -H 'Authorization: Token abcd1234' -c 1 -n 1 http://localhost:5000/open_account/


docker-compose exec mids ab -n 1 -H "Content-Type: application/json" -d '{"user_id": "tpeters", "full_name": "Tim Peters"}' http://localhost:5000/open_account/

docker-compose exec mids ab -p /w205/Project-3-w205-JHR/create_account.txt -T application/json -c 1 -n 1 http://localhost:5000/open_account/

docker-compose exec mids ab -n 1 -T application/json -H "'full_name' : 'Preethi', 'user_id' : 'praju'" http://localhost:5000/open_account

while true;do docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "tpeters", "full_name": "Tim Peters"}' http://localhost:5000/open_account/; sleep 1; done

while true;do docker-compose exec mids curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "tpeters", "full_name": "Tim Peters"}' http://localhost:5000/open_account/; sleep 1; done

while true;do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/create_account.txt -T application/json http://localhost:5000/open_account/; sleep 10; done

#http POST :5000/delete_account/ full_name="Tim Peters" user_id="tpeters"

#http POST :5000/deposit/ user_id="tpeters" amount=200
#http POST :5000/withdraw/ user_id="tpeters" amount=50

#http POST :5000/buy_asset/ user_id="tpeters" number_of=2 asset_name=stock_a
#http POST :5000/sell_asset/ user_id="tpeters" number_of=1 asset_name=stock_a


#Kafka
docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning

#Spark job
docker-compose exec spark spark-submit /w205/Project-3-w205-JHR/writestream_events.py
docker-compose exec spark spark-submit /w205/Project-3-w205-JHR/writestream_account.py

#Hadoop
docker-compose exec cloudera hadoop fs -ls /tmp/
docker-compose exec cloudera hadoop fs -ls /tmp/return_asset_prices

#Apache Bench
while true;do docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/return_price; sleep 10; done

while true;do docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/return_asset_price/stock_a; sleep 10; done


#Hive
docker-compose exec cloudera hive

#Presto
create external table if not exists default.asset_prices (
    raw_event string,
    timestamp string,
    Accept string,
    Host string,
    User_Agent string,
    event_type string,
    description string
  )
  stored as parquet 
  location '/tmp/return_asset_price'
  tblproperties ("parquet.compress"="SNAPPY");
  
create external table if not exists default.account_status (
    raw_event string,
    timestamp string,
    Accept string,
    Host string,
    User_Agent string,
    event_type string,
    description string,
    Content_Length INT,
    Accept_Encoding string,
    Connection string,
    Content_Type string
    
  )
  stored as parquet 
  location '/tmp/account_status'
  tblproperties ("parquet.compress"="SNAPPY");
  
create external table if not exists default.asset_transactions(
    raw_event string,
    timestamp string,
    Accept string,
    Host string,
    User_Agent string,
    event_type string,
    description string,
    Content_Length INT,
    Accept_Encoding string,
    Connection string,
    Content_Type string
)
  stored as parquet 
  location '/tmp/asset_transactions'
  tblproperties ("parquet.compress"="SNAPPY");

create external table if not exists default.cash_transactions( 
    raw_event string,
    timestamp string,
    Accept string,
    Host string,
    User_Agent string,
    event_type string,
    description string,
    Content_Length INT,
    Accept_Encoding string,
    Connection string,
    Content_Type string      
  )
  stored as parquet 
  location '/tmp/cash_transactions'
  tblproperties ("parquet.compress"="SNAPPY");

 
#presto
# show tables;
# describe <table name>;

#docker-compose down 