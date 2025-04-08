**Real-Time Yahoo Finance Data Processing Pipeline**

A scalable pipeline for streaming stock market data using Kafka, Spark, and Cassandra.
This project demonstrates a real-time data processing pipeline using Apache Airflow, Kafka, Spark, and Cassandra. The pipeline is containerized using Docker and orchestrated via Docker Compose.
![architecture](https://github.com/user-attachments/assets/468ba3f9-3a3c-4eae-9025-5526dda74d56)


🔗**Repository:** https://github.com/gadamsr/realtime_dataprocessing

**Overview**
This project implements an end-to-end real-time data pipeline that:
1.	Fetches live stock data from Yahoo Finance API
2.	Streams it through Apache Kafka
3.	Processes it using Spark Structured Streaming
4.	Stores analyzed results in Cassandra
   
 **Technologies Used**

•	**Apache Kafka** – Streaming platform

•	**Apache Spark** – Stream processing

•	**Apache Airflow** – Workflow orchestration

•	**Cassandra** – NoSQL database

•  **Docker & Docker Compose** – Containerization

•  **PostgreSQL** – Metadata DB for Airflow
 
**Project Structure**
.
├── airflow_dags/ kafka_stream  # Custom DAGs for Airflow

├── config/                    # Configuration files

├── docker-compose.yaml        # Main docker-compose config

├── logs/                      # Airflow and Spark logs

├── plugins/                   # Airflow plugins

├── scripts/entrypoint.sh     # Shell scripts or setup helpers

├── architecture.png           # System architecture diagram

├── dependencies.zip           # Spark dependencies

├── requirements.txt           # Python dependencies

├── stream_processor.py        # Spark stream processor

**Setup Instructions**

**1. Clone the Repository**

_git clone https://github.com/gadamsr/realtime_dataprocessing.git_

_cd realtime_dataprocessing_

**2. Set Environment Variables**

_echo -e "AIRFLOW_UID=$(id -u)" > .env_

_echo AIRFLOW_UID=50000 >> .env_

_cd scripts_

_chmod +x scripts/entrypoint.sh_

_ cd .._
 
**3. Initialize Airflow**

_docker-compose up airflow-init_

**4. Start All Services**

_docker-compose up -d_

This launches the following services:
•	Kafka Broker

•	Zookeeper

•	Cassandra

•	Spark Master & Worker

•	Airflow Webserver, Scheduler, Triggerer

•	Kafka UI

•	PostgreSQL (for Airflow metadata)

**5. Upload Project Files to Spark**

Copy project files into the Spark master container:

_docker cp dependencies.zip spark-master:/dependencies.zip_

_docker cp stream_processor.py spark-master:/stream_processor.py_

**6. Access Cassandra**

_docker exec -it cassandra cqlsh -u cassandra -p cassandra localhost 9042_

check if topic was created 

_DESCRIBE KEYSPACES;_

Check if data is being saved in Cassandra

_SELECT * FROM stock_data_streaming.stock_data;_

_SELECT COUNT(*) FROM stock_data_streaming.stock_data;_

**7. Run the Spark Job Using docker exec**

In a new terminal 

_docker exec -it spark-master spark-submit --packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 --py-files /dependencies.zip /stream_processor.py_


 **Airflow UI and Kafka UI**

Once all services are up and running, open the Airflow UI at:

**http://localhost:8080**
unpause DAG to run the job. check Kafka UI to see if the topic has been created and data is being generated. Check cassandra to see if the data is being saved. 

**http://localhost:8085**

Login with:

**Username:** admin

**Password:** admin

**Notes**

•	Make sure Docker is properly installed and running.

•	The .env file is used to pass the UID to Docker for Airflow compatibility.

•	stream_processor.py should define your Spark streaming logic.

•	Kafka topics and DAGs must be created appropriately for the data pipeline to function.

•	To check if all containers are up and healthy use _docker ps -a _

•	To down the containers use _docker-compose down -v_ 



