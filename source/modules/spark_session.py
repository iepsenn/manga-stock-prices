from pyspark.sql import SparkSession
import json
import os
from dotenv import load_dotenv


load_dotenv() 

minio_access_key = os.getenv('MINIO_ACCESS_KEY')
minio_secret_key = os.getenv('MINIO_SECRET_KEY')
minio_endpoint = os.getenv('MINIO_ENDPOINT')

session = (
    SparkSession
    .builder
    .appName("Streaming from Kafka")
    .config("spark.streaming.stopGracefullyOnShutdown", True)
    .config('spark.jars.packages', (
        'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1'
        ',org.apache.spark:spark-avro_2.12:3.5.1'
        ',io.delta:delta-spark_2.12:3.1.0'
        ',org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2'
        ',org.apache.hadoop:hadoop-aws:3.2.4'
        ',org.apache.hadoop:hadoop-common:3.2.4'
    ))
    .config("spark.sql.shuffle.partitions", 4)
    .config('fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
    .config('spark.sql.extensions', ( 
        'io.delta.sql.DeltaSparkSessionExtension'
        ',org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions'
    ))
    .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")
    .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog')
    .config("fs.s3a.access.key", minio_access_key)
    .config("fs.s3a.secret.key", minio_secret_key)
    .config("fs.s3a.endpoint", minio_endpoint)
    .config("fs.s3a.connection.ssl.enabled", "false")
    .config("fs.s3a.path.style.access", "true")
    .config("fs.s3a.connection.ssl.enabled", "false")
    .master("local[*]")
    .getOrCreate()
)
