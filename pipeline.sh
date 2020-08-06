#!/bin/bash

pip install docker-compose
docker-compose up -d

#Check if Kafka is running
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
  
#Kafka
docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning

#Spark job
docker-compose exec spark spark-submit /w205/Project-3-w205-JHR/writestream_events.py
# docker-compose exec spark spark-submit /w205/Project-3-w205-JHR/writestream_account.py

#Hadoop
docker-compose exec cloudera hadoop fs -ls /tmp/
docker-compose exec cloudera hadoop fs -ls /tmp/return_asset_price

#Apache Bench

#default
while true; do docker-compose exec mids ab -n 10 -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/; sleep 1; done

#return all asset prices
while true; do docker-compose exec mids ab -n 10 -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/return_price; sleep 1; done

#return specific asset price
while true; do docker-compose exec mids ab -n 10 -T application/json -H "Host: user1.comcast.com" http://localhost:5000/return_asset_price/stock_a; sleep 1; done

#return account info 
while true; do docker-compose exec mids ab -n 10 -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/return_account_info/tpeters; sleep 1; done

#create account
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/create_account.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/open_account/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/create_account2.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/open_account/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/create_account3.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/open_account/; sleep 1; done

#delete account 
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/delete_account.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/delete_account/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/delete_account2.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/delete_account/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/delete_account3.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/delete_account/; sleep 1; done

#deposit account
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/deposit_amount.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/deposit/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/deposit_amount2.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/deposit/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/deposit_amount3.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/deposit/; sleep 1; done

#withdraw account
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/withdraw_amount.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/withdraw/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/withdraw_amount2.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/withdraw/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/withdraw_amount3.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/withdraw/; sleep 1; done

#buy asset
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/buy_asset.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/buy_asset/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/buy_asset2.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/buy_asset/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/buy_asset3.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/buy_asset/; sleep 1; done

#sell asset
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/sell_asset.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/sell_asset/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/sell_asset2.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/sell_asset/; sleep 1; done
while true; do docker-compose exec mids ab -n 1 -p /w205/Project-3-w205-JHR/test_flask/json_txt_files/sell_asset3.txt -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/sell_asset/; sleep 1; done

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
docker-compose exec presto presto --server presto:8080 --catalog hive --schema default
# show tables;
# describe <table name>;
#select count(*) from asset_prices;

#Tear down cluster 
docker-compose down 



