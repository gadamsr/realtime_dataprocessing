📈 Real-Time Yahoo Finance Data Processing Pipeline
A scalable, real-time data pipeline that ingests, processes, and stores live stock market data using Apache Kafka, Spark, Cassandra, and Airflow, fully containerized with Docker and orchestrated via Docker Compose.

🔗 Repository: github.com/gadamsr/realtime_dataprocessing

📌 Project Overview
This end-to-end real-time data pipeline performs the following:

📥 Fetches live stock data from the Yahoo Finance API

🔄 Streams the data through Apache Kafka

⚡ Processes the stream using Spark Structured Streaming

🗃 Stores the processed data in Cassandra

🔧 Technologies Used
Apache Kafka – Real-time streaming platform

Apache Spark – Structured stream processing

Apache Airflow – Workflow orchestration

Cassandra – Distributed NoSQL database

Docker & Docker Compose – Containerized deployment

PostgreSQL – Metadata database for Airflow

📁 Project Structure
bash
Copy
Edit
.
├── airflow_dags/              # Custom DAGs for Airflow
├── config/                    # Configuration files
├── docker-compose.yaml        # Docker Compose config
├── logs/                      # Airflow and Spark logs
├── plugins/                   # Airflow plugins
├── scripts/entrypoint.sh      # Shell setup scripts
├── architecture.png           # System architecture diagram
├── dependencies.zip           # Spark job dependencies
├── requirements.txt           # Python dependencies
├── stream_processor.py        # Spark streaming processor
🚀 Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/gadamsr/realtime_dataprocessing.git
cd realtime_dataprocessing
2. Set Environment Variables
bash
Copy
Edit
echo -e "AIRFLOW_UID=$(id -u)" > .env
echo AIRFLOW_UID=50000 >> .env
3. Initialize Airflow
bash
Copy
Edit
docker-compose up airflow-init
4. Start All Services
bash
Copy
Edit
docker-compose up -d
This will launch:

Kafka Broker

Zookeeper

Cassandra

Spark Master & Worker

Airflow Webserver, Scheduler, Triggerer

Kafka UI

PostgreSQL (Airflow metadata DB)

5. Upload Project Files to Spark Container
bash
Copy
Edit
docker cp dependencies.zip spark-master:/dependencies.zip
docker cp stream_processor.py spark-master:/stream_processor.py
6. Access Cassandra
bash
Copy
Edit
docker exec -it cassandra cqlsh -u cassandra -p cassandra localhost 9042
Run the following CQL commands to verify:

sql
Copy
Edit
DESCRIBE KEYSPACES;
SELECT * FROM stock_data_streaming.stock_data;
SELECT COUNT(*) FROM stock_data_streaming.stock_data;
7. Run the Spark Streaming Job
In a new terminal:

bash
Copy
Edit
docker exec -it spark-master spark-submit \
  --packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.1,\
org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  --py-files /dependencies.zip \
  /stream_processor.py
📊 Interfaces
Airflow UI
📍 http://localhost:8080
Login:

Username: admin

Password: admin

Kafka UI
📍 http://localhost:8085

📝 Notes
Ensure Docker is installed and running.

.env file helps pass the correct user ID to Airflow.

stream_processor.py contains the core Spark streaming logic.

Kafka topics and Airflow DAGs must be defined before running.

Check container status:

bash
Copy
Edit
docker ps -a
Stop all containers:

bash
Copy
Edit
docker-compose down -v
