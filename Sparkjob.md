# Project 3 - Report 2: Spark Job

- This is the 2nd of the 3 reports for project 2. The 1st report is an overview of our pipeline design. In this report , we describe the spark job to stream metadata from our "banking game" app. 

We track 4 types of events from Kafka queue in the spark stream job and land them into 4 tables in hive. 
We start with an understanding of the metadata from the app. They are:
- price/account inquiries: users can choose to see prices of all assets available in the app, or specify the name of the asset, such as "stock_a", or "bond_b". Users can also query the account info for his/her account.
- asset transactions: users can sell or buy a stock or a bond
- cash transactions: users can deposit or withdraw cash
- account status: Users can open, close an account. 

As such, the first functions in the spark job are to define the schema for each event type. For events that are related to the same transactional nature and share the same schema, such as "depoist" and "withdrawal", they are grouped under the same structure. 4 schemas are defined, matching the event type list above. 

Next, we created functions to identify the events as "Yes" or "No", to be used in the main function to filter the incoming data by event types.

Finally, in the "main" function, we take the "raw data" from Kafka queue using "readStream" function, filter by event type, cast the type as "string", apply the related schema and use "writeStream" to output the data into a parquet file and save it under a subfolder under "tmp" in Cloudera. Each subfolder represents a group of events. In total, we created 4 subfolders. 
- return_asset_price: holds all price/account inquiries
- account_status : holds account open/close activities
- asset_transactions : holds asset buy/sell activities
- cash_transactions: holds cash deposit/withdrawal activities

In the Spark portion of our project, we tried advance option #1. 

- Generate and filter more types of events.  There are plenty of other things
  you might capture events for during gameplay

The final report will be a business analytics report of the data in Hive tables. 

