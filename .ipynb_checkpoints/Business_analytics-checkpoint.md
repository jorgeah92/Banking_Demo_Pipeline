# Business Analytics Verification

Now that the pipeline has been constructed and information is being passed through to the database, we want to verify that everything is working properly. We will verify the database by answering a few questions using the information from each of the tables we created.

#### Are users showing interest in the application?

To answer this question, we will conduct a query in presto to see the number of deposits and withdraws used so far:

`presto:default> select event_type, count(event_type) from cash_transactions group by event_type;`

   event_type    | _col1 
-----------------+-------
 make_withdrawal |  210 
 make_deposit    |  300 
(2 rows)

Query 20200804_012436_00007_i4zqf, FINISHED, 1 node
Splits: 32 total, 25 done (78.13%)
0:01 [174 rows, 79.8KB] [159 rows/s, 72.9KB/s]

It seems that users are using showing interest in the application as the deposit function is being utilized more than withdraw function, which can imply that users are more actively investing using the application.


#### What asset options are being purchased the most?
To answer this question, we will examine the asset table for the top most purchased assets:

`presto:default> select description, count(description) from asset_transactions group by description;`

 description | _col1 
-------------+-------
 stock_a 2   |    27 
 bond_a 2    |    20 
 bond_a 10   |    19 
 stock_a 10  |    26 
(4 rows)

Query 20200804_024251_00007_3wzau, FINISHED, 1 node
Splits: 71 total, 70 done (98.59%)
0:04 [92 rows, 48.9KB] [24 rows/s, 13.1KB/s]

stock_a is being purchased the most frequently, followed closely by bond_a.

#### What assets are being viewed the most?
To answer this question, we will look at the asset_prices table and examine the top most viewed assets:

`presto:default> select description, count(description) from asset_prices group by description;`

         description         | _col1 
-----------------------------+-------
 stock_a                     |  1050 
 Return price for all assets |  1130 
(2 rows)

Query 20200804_024514_00009_3wzau, FINISHED, 1 node
Splits: 78 total, 65 done (83.33%)
0:01 [1.71K rows, 53.2KB] [1.24K rows/s, 38.7KB/s]

Viewing all of the assets prices is the most used option followed by examining the price of stock_a alone.

#### What is our user retention?
To answer this question, we will look at the number of accounts created versus the number of accounts deleted so far:

`presto:default> select event_type, count(event_type) from account_status group by event_type;`


   event_type   | _col1 
----------------+-------
 open_account   |   201 
 delete_account |   199 
(2 rows)

Query 20200804_024125_00006_3wzau, FINISHED, 1 node
Splits: 62 total, 56 done (90.32%)
0:04 [376 rows, 133KB] [98 rows/s, 34.8KB/s]

It seems that the number of accounts created and deleted are roughly the same which means that we are not retaining users and would need to conduct research to address this serious issue.