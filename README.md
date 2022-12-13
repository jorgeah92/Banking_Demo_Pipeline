# Banking Demo API Pipeline Network
w205 project 3 repo for Jing, Hernandez, and Raju

A demo web application that mimics a simple banking interface built using Docker. The banking interface was built in Python using Flask for web calls. Each time a call is made by the user a event is created and sent through a pipeline to its ultimate destination of HDFS for storage. The events messages are queued with Kafka in order to be streamed to Spark, as an ingestion service. Spark is used to filter, flatten, and transform the streamed information to better suit storage in HDFS. Docker-compose and a yaml file was used for spinning up the Docker cluster as well as connecting all the individual programs. Cloudera was the version of HDFS used for this project and Zookeeper was used as the broker for Kafka. Presto was ran in the cluster as well so that SQL queries can be ran from the generated data of the banking application.


This repo is composed of several files used to build our pipeline for transfering information from a web application to databased storage in HDFS to be used with presto.

1. banking_game_api.py - This is a flask application written as a python script that allows a user to call commands through a web address.
2. docker-comppose.yml - A yml file that contains all of the parameters for the docker containers utilized in this pipeline
3. writestream_events.py - A spark job file that allows spark to operate in a streaming mode to extract information from a Kafka topic and place the information into HDFS
4. pipeline.sh - This is a shell file that contains all of the cml commands to construct the pipeline from scratch
5. Project_3_Instructions.md - The written instructions for Project 3 w205
6. /tmp folder - A destination for a json file created by the flask application for temporary storage of information
7. /test_flask folder - A folder that contains several json that are needed to run Apache Bench commands with the flask application
8. Business_analytics.md - A short report that verifies the construction of the database through several queries conducted in presto
9. Sparkjob.md - A document that describes the spark job (writestream_events.py) in more detail
10. Pipeline.md - A document that describes the entire pipeline (commands in pipeline.sh).
