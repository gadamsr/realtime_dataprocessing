import logging
from datetime import datetime
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Cassandra keyspace
def create_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS stock_data_streaming
        WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """)
    logger.info("Keyspace created successfully")

# Create Cassandra table for stock data
def create_table(session):
    session.execute("""
        CREATE TABLE IF NOT EXISTS stock_data_streaming.stock_data (
            symbol TEXT,
            timestamp TEXT,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume INT,
            PRIMARY KEY (symbol, timestamp)
        );
        """)
    logger.info("Table created successfully")

# Create Spark connection
def create_spark_connection():
    try:
        spark_conn = SparkSession.builder \
            .appName('StockDataStreaming') \
            .config('spark.jars.packages', "com.datastax.spark:spark-cassandra-connector_2.12:3.5.1,"
                                           "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
            .config('spark.cassandra.connection.host', 'cassandra') \
            .getOrCreate()
        spark_conn.sparkContext.setLogLevel("ERROR")
        logger.info("Spark connection created successfully")
        return spark_conn
    except Exception as e:
        logger.error(f"Error while creating Spark connection: {e}")
        return None

# Connect to Kafka
def connect_to_kafka(spark_conn):
    try:
        spark_df = spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'broker:9092') \
            .option('subscribe', 'stock_data') \
            .option('startingOffsets', 'earliest') \
            .load()
        logger.info("Kafka dataframe created successfully")
        return spark_df
    except Exception as e:
        logger.error(f"Error while connecting to Kafka: {e}")
        return None

# Create Cassandra connection
def create_cassandra_connection():
    try:
        cluster = Cluster(['cassandra'])
        cas_session = cluster.connect()
        logger.info("Cassandra connection created successfully")
        return cas_session
    except Exception as e:
        logger.error(f"Error while creating Cassandra connection: {e}")
        return None

# Process Kafka data into structured format
def create_selection_df_from_kafka(spark_df):
    schema = StructType([
        StructField("symbol", StringType(), False),
        StructField("timestamp", StringType(), False),
        StructField("open", FloatType(), False),
        StructField("high", FloatType(), False),
        StructField("low", FloatType(), False),
        StructField("close", FloatType(), False),
        StructField("volume", IntegerType(), False)
    ])

    sel = spark_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")
    logger.info("Selection dataframe created successfully")
    return sel

if __name__ == "__main__":
    spark_conn = create_spark_connection()
    
    if spark_conn:
        spark_df = connect_to_kafka(spark_conn)
        if spark_df:
            selection_df = create_selection_df_from_kafka(spark_df)
            selection_df.printSchema()
            
            session = create_cassandra_connection()
            if session:
                create_keyspace(session)
                create_table(session)

                streaming_query = selection_df.writeStream.format("org.apache.spark.sql.cassandra") \
                    .option('keyspace', 'stock_data_streaming') \
                    .option('checkpointLocation', '/tmp/checkpoint') \
                    .option('table', 'stock_data') \
                    .start()
                
                streaming_query.awaitTermination()
                session.shutdown()

