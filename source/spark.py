import os
from pyspark.sql.functions import col
from dotenv import load_dotenv
from modules import (
    get_symbol,
    get_last_price,
    get_timestamp,
    get_volume,
    get_trade_conditions
)
from modules import session


load_dotenv() 

# Variables
kafka_servers = os.getenv('KAFKA_SERVERS').split(',')
bucket = os.getenv('SOURCE_BUCKET')
table_name = os.getenv('DELTA_TABLE_NAME')

delta_table_path = f"s3a://{bucket}/{table_name}"
delta_logs_path = f"s3a://{bucket}/logs/"

try:
    query = (
        session.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", kafka_servers[0])
        .option("subscribe", "price")
        .option("startingOffsets", "earliest")
        .load()
        .withColumn("symbol", get_symbol(col("value")))
        .withColumn("last_price", get_last_price(col("value")))
        .withColumn("timestamp", get_timestamp(col("value")))
        .withColumn("volume", get_volume(col("value")))
        .withColumn("trade_conditions", get_trade_conditions(col("value")))
        .select("symbol", "last_price", "timestamp", "volume", "trade_conditions") 
        .writeStream
        .format("delta")
        .outputMode("append")
        .option("mergeSchema", "true")
        .option("checkpointLocation", delta_logs_path)
        .trigger(processingTime="10 seconds")
        .start(delta_table_path)
        .awaitTermination()
    )
except Exception as e:
    print(f"Error: {e.message}")
session.stop()
