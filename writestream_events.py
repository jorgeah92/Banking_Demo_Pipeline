#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def return_event_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- timestamp: string(nullable = true)
    |-- description: string (nullable = true)
    
    """
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("description",StringType(), True),
        StructField("timestamp",StringType(), True),
    ])

def account_event_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- timestamp: string (nullable = true)
    |-- description: string (nullable = true)
    |-- Content-Length: IntegerType (nullable = true)
    |-- Accept-Encoding: string (nullable = true)
    |-- Connection: string (nullable = true)
    |-- Content-Type: string(nullable = true)
       
    """
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("description",StringType(), True),
        StructField("Content-Length", IntegerType(), True),
        StructField("Accept-Encoding", StringType(), True),
        StructField("Connection", StringType(), True),
        StructField("Content-Type",StringType(), True),
        StructField("timestamp",StringType(), True),
    ])

def asset_transactions_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- timestamp: string (nullable = true)
    |-- description: string (nullable = true)
    |-- Content-Length: IntegerType (nullable = true)
    |-- Accept-Encoding: string (nullable = true)
    |-- Connection: string (nullable = true)
    |-- Content-Type: string(nullable = true)
       
    """
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("description",StringType(), True),
        StructField("Content-Length", IntegerType(), True),
        StructField("Accept-Encoding", StringType(), True),
        StructField("Connection", StringType(), True),
        StructField("Content-Type",StringType(), True),
        StructField("timestamp",StringType(), True),
    ])

def cash_transactions_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- timestamp: string (nullable = true)
    |-- description: string (nullable = true)
    |-- Content-Length: IntegerType (nullable = true)
    |-- Accept-Encoding: string (nullable = true)
    |-- Connection: string (nullable = true)
    |-- Content-Type: string(nullable = true)
       
    """
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("description",StringType(), True),
        StructField("Content-Length", IntegerType(), True),
        StructField("Accept-Encoding", StringType(), True),
        StructField("Connection", StringType(), True),
        StructField("Content-Type",StringType(), True),
        StructField("timestamp",StringType(), True),
    ])

@udf('boolean')
def is_return_event(event_as_json):
    """udf for filtering return asset price events
    """
    event = json.loads(event_as_json)
    if event['event_type'] in  ['return_asset_price','return_account_info']:
        return True
    return False

@udf('boolean')
def is_account_event(event_as_json):
    """udf for filtering account open and account close events
    """
    event = json.loads(event_as_json)
    if event['event_type'] in ['delete_account','open_account']:
        return True
    return False

@udf('boolean')
def is_asset_transactions(event_as_json):
    """udf for filtering purchases and sales events
    """
    event = json.loads(event_as_json)
    if event['event_type'] in ['buy_asset','sell_asset']:
        return True
    return False

@udf('boolean')
def is_cash_transactions(event_as_json):
    """udf for filtering deposit and withdrawal events
    """
    event = json.loads(event_as_json)
    if event['event_type'] in ['make_deposit','make_withdrawal']:
        return True
    return False

def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \
        .load()

    return_asset_price = raw_events \
        .filter(is_return_event(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          return_event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')
    
#     return_asset_price.printSchema()
#     return_asset_price.show(100)
    
    sink1 = return_asset_price \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_return_asset_price") \
        .option("path", "/tmp/return_asset_price") \
        .trigger(processingTime="10 seconds") \
        .start()

    sink1.awaitTermination()
    
    account_status = raw_events \
        .filter(is_account_event(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          account_event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')

#     account_status.printSchema()
#     account_status.show(100)
    
    sink2 = account_status \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_account_status") \
        .option("path", "/tmp/account_status") \
        .trigger(processingTime="10 seconds") \
        .start()

    sink2.awaitTermination()
    
    asset_transactions = raw_events \
        .filter(is_asset_transactions(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          asset_transactions_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')

#     asset_transactions.printSchema()
#     asset_transactions.show(100)
    
    sink3 = asset_transactions \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_asset_transactions") \
        .option("path", "/tmp/asset_transactions") \
        .trigger(processingTime="10 seconds") \
        .start()

    sink3.awaitTermination()
    
    cash_transactions = raw_events \
        .filter(is_cash_transactions(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          cash_transactions_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')

#     cash_transactions.printSchema()
#     cash_transactions.show(100)
    
    sink4 = cash_transactions \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_cash_transactions") \
        .option("path", "/tmp/cash_transactions") \
        .trigger(processingTime="10 seconds") \
        .start()

    sink4.awaitTermination()



if __name__ == "__main__":
    main()