## Pipeline

The aim of our pipeline is to create a docker container through which we want to consume and transform messages in Spark so we can read them in HDFS. 

Kafka will serve as the queue in order to read / stream the messages into our stream ingestion service, Spark. We chose Spark because of its rapid  lazy evaluation properties, which are only enhanced by the optimization of SQL. Spark with filter/flatten/transform these events and write them to storage- Hadoop. Here, we use Cloudera, the most popular distribution of Hadoop. 

Since we are using multiple services, we will use a yaml file to spin up a cluster that came with Kafka, Cloudera, Zookeeper, Spark and MIDS (an open-source container created on docker hub). We had to connect the required services via ports (which expose the service to the host and allow connections amongst services). This ultimately creates a spark stack with kafka and HDFS. We also had to add volumes to the yaml file; this ensures changes made inside a docker container to our folder (here w205) in the host machine. 


```shell 
mkdir w205
```

Spin up the pipeline and allow it to run in the background using -d tag: 

```shell 
docker-compose up -d
```

Check the logs for Kafka to make sure this container is running properly. 

```shell 
docker-compose logs -f kafka
```
Create a Kafka topic called **events** with user events; this topic will be hosted on a Kafka server so the messages can be consumed, transformed, and read by Spark. 


```shell 
 docker-compose exec kafka \
   kafka-topics \
     --create \
     --topic events \
     --partitions 1 \
     --replication-factor 1 \
     --if-not-exists \
     --zookeeper zookeeper:32181
     
```

Zookeeper is the broker for Kafka, used to store metadata. During topic creation, we specify the zookeeper port from the yaml file to connect Kafka and Zookeeper. Zookeeper keeps track of Kafka partitions and replications of the data (here both are 1). The former enables producer and consumer loads to be scaled, which we would consider if we had more data to consume; the latter is used to combat failovers or access the data again. 

Now execute an interactive bash shell on the mids container. Let's run the Flask app locally: 

```shell 
docker-compose exec mids \
  env FLASK_APP=/w205/Project-3-w205-JHR/banking_game_api.py \
  flask run --host 0.0.0.0
```

User actions will be mapped to API endpoints (i.e. GET /return_price to return the price of all assets). The API contains code to log the events and descriptions to Kafka. 

Use kafkacat to consume events from the "events" topic, which are then read from Kafka. Notice leaving out the '-e' switch will cause this to run continuously in our terminal. 

```shell
docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning
```

Run the Spark job (see *Sparkjob.md* for a full explaination). This report describes the spark job to stream metadata from our "banking game" app. We track 4 types of events from Kafka queue in the spark stream job and land them into 4 tables in hive. Our pyspark code is captured in *writestream_events.py*. Using the below shell command, we will create the Spark session and deploy our Spark job to a cluster. 

```shell
docker-compose exec spark spark-submit /w205/Project-3-w205-JHR/writestream_events.py
```

Spark then pulls events from kafka, filters/flattens/transforms events, and writes them to storage (Cloudera, a version of Hadoop), so presto then can be used to query those events. 

We can check our parquet files for the API results in HDFS.  

```shell
docker-compose exec cloudera hadoop fs -ls /tmp/
docker-compose exec cloudera hadoop fs -ls /tmp/return_asset_price
```

Use Apache Bench to continuously generate events for testing purposes. See the rest of the Apache Bench commands in pipeline.sh. 

```shell
while true; do docker-compose exec mids ab -n 10 -T application/json  -H "Host: user1.comcast.com" http://localhost:5000/return_price; sleep 1; done
```

The Hive metastore is a really common tool used to keep track of schema for tables used throughout the Hadoop and Spark ecosystem (schema registry). To "expose" the schema for our events, we need to create a table in the hive metastore. We simply use the schema registry for Hive (we don't use the full query engine since it's slow). The hive metastore is friendly with multiple partitions being stored. We write our events with spark and while we want to read them with presto, to get them to agree we track the schema with hive metastore. 

We have a hive metastore spun up in our cloudera container (which is why we need a new cloudera container). 


```shell
docker-compose exec cloudera hive
```

Let's create our tables in the Hive metastore. 

```shell
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

 
```

We can then query our data in presto. 

Presto is a query engine that talks to the the hive thrift server to get the tables we just added; specifically it connecgts to HDSFS to get the data. 

We query with presto instead of spark bc presto scales well, handles a wider range of SQL syntax, can be treated immediately like a database, and can be configured to talk to a data lake immediately. 

```shell
docker-compose exec presto presto --server presto:8080 --catalog hive --schema default
show tables;
describe asset_prices;
select count(*) from asset_prices;
```

Tear down your cluster when finished. 

```shell
docker-compose down 
```