# Project-3-w205-JHR
w205 project 3 repo for Jing, Hernandez, and Raju

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
10. 