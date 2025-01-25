### Stock Stream Processing

by: 
- Amin Haeri
- Alireza Nazari 


- commit the work done till now
- create a redis database and pod for it
- update the stream processor code to write on the redis (if it didn't work for the first time use a simple python code)
- test the redis to see if it has the data
- commit the redis database 
- commit the new stream processor
- update the task if done under 2 hours

TODO LIST:
- optional: improve the stream processor deploy script by moving the config options from the script into the pod config
OR add a config map and use SPARK_CONF_FILE to point to it
- docs: add a system object in icepanel to show the endpoint 
- do: add resources for pod config, specially the spark workers and driver
- optional: add a python code that act as reverse proxy for spark ui
- docs: create a good readme
- do: make sure the kafka is partitions and replicas are at best value
- do: use immutable image tag instead of latest 
