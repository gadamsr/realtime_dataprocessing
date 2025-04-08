**Real-Time Yahoo Finance Data Processing Pipeline**
A scalable pipeline for streaming stock market data using Kafka, Spark, and Cassandra.
This project demonstrates a real-time data processing pipeline using Apache Airflow, Kafka, Spark, and Cassandra. The pipeline is containerized using Docker and orchestrated via Docker Compose.

🔗**Repository:** https://github.com/gadamsr/realtime_dataprocessing

📌**Overview**
This project implements an end-to-end real-time data pipeline that:
1.	Fetches live stock data from Yahoo Finance API
2.	Streams it through Apache Kafka
3.	Processes it using Spark Structured Streaming
4.	Stores analyzed results in Cassandra
   
🔧 **Technologies Used**

•	**Apache Kafka** – Streaming platform
•	**Apache Spark** – Stream processing
•	**Apache Airflow** – Workflow orchestration
•	**Cassandra** – NoSQL database
•**Docker & Docker Compose** – Containerization
•**PostgreSQL** – Metadata DB for Airflow
 
**Project Structure**
.
├── airflow_dags/ kafka_stream             # Custom DAGs for Airflow
├── config/                    # Configuration files
├── docker-compose.yaml        # Main docker-compose config
├── logs/                      # Airflow and Spark logs
├── plugins/                   # Airflow plugins
├── scripts/entrypoint.sh                   # Shell scripts or setup helpers
├── architecture.png           # System architecture diagram
├── dependencies.zip           # Spark dependencies
├── requirements.txt           # Python dependencies
├── stream_processor.py        # Spark stream processor

**🚀 Setup Instructions**

**1. Clone the Repository**
git clone https://github.com/gadamsr/realtime_dataprocessing.git
cd realtime_dataprocessing
2. Set Environment Variables
echo -e "AIRFLOW_UID=$(id -u)" > .env
echo AIRFLOW_UID=50000 >> .env

**3. Initialize Airflow**
docker-compose up airflow-init

**4. Start All Services**
docker-compose up -d
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
docker cp dependencies.zip spark-master:/dependencies.zip
docker cp stream_processor.py spark-master:/stream_processor.py

**6. Access Cassandra**
docker exec -it cassandra cqlsh -u cassandra -p cassandra localhost 9042
check if topic was created 
DESCRIBE KEYSPACES;
Check if data is being saved in Cassandra
SELECT * FROM stock_data_streaming.stock_data;
SELECT COUNT(*) FROM stock_data_streaming.stock_data;

**7. Run the Spark Job Using docker exec**
In a new terminal 
docker exec -it spark-master spark-submit --packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 --py-files /dependencies.zip /stream_processor.py

📊 **Airflow UI and Kafka UI**
Once all services are up and running, open the Airflow UI at:
http://localhost:8080
http://localhost:8085

Login with:

•**Username:** admin

•**Password:** admin

📌**Notes**
•	Make sure Docker is properly installed and running.
•	The .env file is used to pass the UID to Docker for Airflow compatibility.
•	stream_processor.py should define your Spark streaming logic.
•	Kafka topics and DAGs must be created appropriately for the data pipeline to function.
•	To check if all containers are up and healthy use docker ps -a 
•	To down the containers use docker-compose down -v 



