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
#docker-compose exec mids curl http://localhost:5000/return_account_info/tpeters

#http POST :5000/open_account/ full_name="Tim Peters" user_id="tpeters"
#http POST :5000/delete_account/ full_name="Tim Peters" user_id="tpeters"

#http POST :5000/deposit/ user_id="tpeters" amount=200
#http POST :5000/withdraw/ user_id="tpeters" amount=50

#http POST :5000/buy_asset/ user_id="tpeters" number_of=2 asset_name=stock_a
#http POST :5000/sell_asset/ user_id="tpeters" number_of=1 asset_name=stock_a


#Kafka
docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning

#Spark job
docker-compose exec spark spark-submit /w205/Project-3-w205-JHR/writestream_events.py

#Hadoop
docker-compose exec cloudera hadoop fs -ls /tmp/

#Apache Bench
while true;do docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http://localhost:5000/return_price; sleep 10; done

# while true;do docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" http POST :5000/open_account/ full_name="Tim Peters" user_id="tpeters"; sleep 10; done

# while true;do docker-compose exec mids ab -n 5 -H "Host: user1.comcast.com" http POST :5000/delete_account/ full_name="Tim Peters" user_id="tpeters"; sleep 10; done

# while true;do docker-compose exec mids ab -n 5 -H "Host: user1.comcast.com" http POST :5000/deposit/ user_id="tpeters" amount=200; sleep 10; done

# while true;do docker-compose exec mids ab -n 5 -H "Host: user1.comcast.com" http POST :5000/buy_asset/ user_id="tpeters" number_of=2 asset_name=stock_a; sleep 10; done

#Hive
docker-compose exec cloudera hive

#Presto
create external table if not exists default.asset_prices (
   
    Host string,
    User_Agent string,
    event_type string,
    Accept string,
    description string,
    timestamp string,
    raw_event string
  )
  stored as parquet 
  location '/tmp/return_asset_price'
  tblproperties ("parquet.compress"="SNAPPY");
  
create external table if not exists default.account_status (
    Accept string,
    Host string,
    User_Agent string,
    event_type string,
    description string,
    Content-Length string,
    Accept-Encoding string,
    Connection string,
    Content-Type string,
    timestamp string,
    raw_event string
  )
  stored as parquet 
  location '/tmp/account_status'
  tblproperties ("parquet.compress"="SNAPPY");
  
create external table if not exists default.asset_transactions(
    Accept string,
    Host string,
    User_Agent string,
    event_type string,
    description string,
    Content-Length string,
    Accept-Encoding string,
    Connection string,
    Content-Type string,
    timestamp string,
    raw_event string
  )
  stored as parquet 
  location '/tmp/asset_transactions'
  tblproperties ("parquet.compress"="SNAPPY");

create external table if not exists default.cash_transactions(
    Accept string,
    Host string,
    User_Agent string,
    event_type string,
    description string,
    Content-Length string,
    Accept-Encoding string,
    Connection string,
    Content-Type string,
    timestamp string,
    raw_event string
  )
  stored as parquet 
  location '/tmp/cash_transactions'
  tblproperties ("parquet.compress"="SNAPPY");


  
#presto
# show tables;
# describe <table name>;

#docker-compose down 

