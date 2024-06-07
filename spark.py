from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, LongType
import json


sourceBucket = "warehouse"
deltaTablePath = f"s3a://{sourceBucket}/test"

get_symbol = udf(lambda x: json.loads(x)['symbol'], StringType())
get_last_price = udf(lambda x: json.loads(x)['last_price'], StringType())
get_timestamp = udf(lambda x: json.loads(x)['timestamp'], StringType())
get_volume = udf(lambda x: json.loads(x)['volume'], StringType())
get_trade_conditions = udf(lambda x: json.loads(x)['trade_conditions'], StringType())

spark = (
    SparkSession
    .builder
    .appName("Streaming from Kafka")
    .config("spark.streaming.stopGracefullyOnShutdown", True)
    .config('spark.jars.packages', (
        'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1'
        ',org.apache.spark:spark-avro_2.12:3.5.1'
        ',io.delta:delta-spark_2.12:3.1.0'
        # ',org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.3.1'
        ',org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2'
        ',org.projectnessie.nessie-integrations:nessie-spark-extensions-3.3_2.12:0.67.0'
        ',org.apache.hadoop:hadoop-aws:3.2.4'
        ',org.apache.hadoop:hadoop-common:3.2.4'
    ))
    .config("spark.sql.shuffle.partitions", 4)
    .config('fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
    .config('spark.sql.extensions', ( 
        'io.delta.sql.DeltaSparkSessionExtension'
        ',org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions'
        ',org.projectnessie.spark.extensions.NessieSparkSessionExtensions'
    ))
    .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")
    .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog')
    .config("fs.s3a.access.key", "accesskey")
    .config("fs.s3a.secret.key", "secretkey")
    .config("fs.s3a.endpoint", "http://minio:9000")
    .config("fs.s3a.connection.ssl.enabled", "false")
    .config("fs.s3a.path.style.access", "true")
    .config("fs.s3a.connection.ssl.enabled", "false")
    .config('spark.sql.catalog.nessie', 'org.apache.iceberg.spark.SparkCatalog')
    .config('spark.sql.catalog.nessie.uri', 'http://nessie:19120/api/v1')
    .config('spark.sql.catalog.nessie.ref', 'main')
    .config('spark.sql.catalog.nessie.authentication.type', 'NONE')
    .config('spark.sql.catalog.nessie.catalog-impl', 'org.apache.iceberg.nessie.NessieCatalog')
    .config('spark.sql.catalog.nessie.s3.endpoint', 'http://minio:9000')
    .config('spark.sql.catalog.nessie.warehouse', f's3a://{sourceBucket}/')
    .config('spark.sql.catalog.nessie.io-impl', 'org.apache.iceberg.aws.s3.S3FileIO')
    .master("local[*]")
    .getOrCreate()
)


# streaming_df = spark.readStream\
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "Kafka00Service:9092") \
#     .option("subscribe", "price") \
#     .option("startingOffsets", "earliest") \
#     .load()

# print('STREAMING DF ====> \n')
# streaming_df.printSchema()
# streaming_df

# query = (
#     streaming_df
#     .withColumn("symbol", get_symbol(col("value")))
#     .withColumn("last_price", get_last_price(col("value")))
#     .withColumn("timestamp", get_timestamp(col("value")))
#     .withColumn("volume", get_volume(col("value")))
#     .withColumn("trade_conditions", get_trade_conditions(col("value")))
#     .select("symbol", "last_price", "timestamp", "volume", "trade_conditions") 
#     .writeStream
#     .format("console")
#     .start()
# )
# print('QUERY ====> \n')
# query
# query.awaitTermination()

# sourceBucket = "lake"
# deltaTablePath = f"s3a://{sourceBucket}/test"

query = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "Kafka00Service:9092")
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
    .option("checkpointLocation", f"s3a://{sourceBucket}/logs/")
    .trigger(processingTime="30 seconds")
    .start(deltaTablePath)
    .awaitTermination()
)
# print('QUERY ====> \n')
# query
# query.awaitTermination()
# .option("checkpointLocation", f"s3a://{sourceBucket}/logs/")
#     .start(deltaTablePath)
# .option("checkpointLocation", "/home/ddelta/logs")
#     .start("/home/ddelta/table")
spark.stop()


#https://docs.databricks.com/en/structured-streaming/delta-lake.html


  