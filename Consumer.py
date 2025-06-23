import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, DoubleType, LongType
from pyspark.sql.functions import from_json, col

# ✅ Disable native Hadoop library access on Windows
os.environ["HADOOP_OPTS"] = "-Djava.library.path="

# ✅ Create Spark session with necessary configs
spark = SparkSession.builder \
    .appName("KafkaConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
    .config("spark.sql.shuffle.partitions", "2") \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .getOrCreate()

# ✅ Define schema for Kafka JSON value
schema = StructType() \
    .add("device_id", StringType()) \
    .add("temperature", DoubleType()) \
    .add("humidity", DoubleType()) \
    .add("timestamp", LongType())

# ✅ Read from Kafka topic
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "iot") \
    .option("startingOffsets", "latest") \
    .load()

# ✅ Convert Kafka value (binary) to string and parse JSON
df_parsed = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# ✅ Write to console and set a Windows-friendly checkpoint location
query = df_parsed.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("checkpointLocation", "file:///C:/Users/geeta/spark-checkpoints") \
    .start()

query.awaitTermination()
