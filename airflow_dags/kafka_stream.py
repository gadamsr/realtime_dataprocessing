from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import yfinance as yf
import logging
import json
import time
from kafka import KafkaProducer
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

default_args = {
    'owner': 'admin',
    'start_date': datetime(2023, 9, 3, 10, 00),
    'retries': 3,  # Automatically retry failed tasks 3 times
    'retry_delay': timedelta(minutes=5),  # Retry delay
}

# List of stock symbols (Replace with a complete list from an API or CSV)
symbols = ["AAPL", "SES", "BIDU", "BABA", "IIPR", "ANTE", "BTCRX", "BTC-USD", "PLTR", "QBTS", "LCID", "GOOG", "MSFT", "AMZN", "TSLA", "NVDA", "META", "NFLX", "INTC", "AMD"]

# Function to fetch daily stock data for the last year
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1y", interval="1d")  # Fetch daily data for the past year

        if hist.empty:
            logger.warning(f"No data fetched for {symbol}.")
            return None

        records = []
        for index, row in hist.iterrows():
            data = {
                "symbol": symbol,
                "timestamp": index.strftime('%Y-%m-%d'),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": int(row["Volume"])
            }
            records.append(data)

        logger.info(f"Fetched {len(records)} records for {symbol}.")
        return records

    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return None

# Function to stream data to Kafka
def stream_data():
    producer = KafkaProducer(bootstrap_servers='broker:9092', max_block_ms=5000)

    with ThreadPoolExecutor(max_workers=5) as executor:  # Fetch multiple stocks in parallel
        futures = {symbol: executor.submit(get_stock_data, symbol) for symbol in symbols}

        for symbol, future in futures.items():
            try:
                records = future.result()
                if records:
                    for record in records:
                        producer.send('stock_data', json.dumps(record).encode('utf-8'))
                    logger.info(f"Sent {len(records)} records for {symbol} to Kafka")
            except Exception as e:
                logger.error(f"Error streaming data for {symbol}: {e}")

    logger.info("Completed streaming historical stock data to Kafka.")

# Define the Airflow DAG
with DAG('stock_data_historical',
         default_args=default_args,
         schedule_interval='@once',  # Run this DAG once to fetch historical data
         catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='stream_historical_stock_data_to_kafka',
        python_callable=stream_data
    )

