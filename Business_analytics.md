presto:default> select event_type, count(event_type) from cash_transactions group by event_type;
   event_type    | _col1 
-----------------+-------
 make_withdrawal |  2120 
 make_deposit    |  3040 
(2 rows)

Query 20200804_012436_00007_i4zqf, FINISHED, 1 node
Splits: 32 total, 25 done (78.13%)
0:01 [174 rows, 79.8KB] [159 rows/s, 72.9KB/s]

presto:default> select event_type, count(event_type) from account_status group by event_type;
   event_type   | _col1 
----------------+-------
 open_account   |   201 
 delete_account |   199 
(2 rows)

Query 20200804_024125_00006_3wzau, FINISHED, 1 node
Splits: 62 total, 56 done (90.32%)
0:04 [376 rows, 133KB] [98 rows/s, 34.8KB/s]

presto:default> select description, count(description) from asset_transactions group by description;
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

presto:default> select description, count(description) from asset_prices group by description;
         description         | _col1 
-----------------------------+-------
 stock_a                     |  1050 
 Return price for all assets |  1130 
(2 rows)

Query 20200804_024514_00009_3wzau, FINISHED, 1 node
Splits: 78 total, 65 done (83.33%)
0:01 [1.71K rows, 53.2KB] [1.24K rows/s, 38.7KB/s]
