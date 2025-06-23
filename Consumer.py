import os
import joblib
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, DoubleType, LongType
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.functions import struct
from pyspark.sql.types import IntegerType

# Load your Isolation Forest model
model = joblib.load("anomaly_model.pkl")

# UDF to apply the ML model
def detect_anomaly(temp, hum):
    features = np.array([[temp, hum]])
    prediction = model.predict(features)
    return int(prediction[0])  # -1 for anomaly, 1 for normal

# Register the UDF with PySpark
from pyspark.sql.functions import pandas_udf
@pandas_udf(IntegerType())
def detect_anomaly_udf(temp, hum):
    return [detect_anomaly(t, h) for t, h in zip(temp, hum)]

# Disable native Hadoop lib (Windows)
os.environ["HADOOP_OPTS"] = "-Djava.library.path="

# Create Spark session
spark = SparkSession.builder \
    .appName("KafkaConsumerWithAnomalyDetection") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
    .config("spark.sql.shuffle.partitions", "2") \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .getOrCreate()

# Define the schema
schema = StructType() \
    .add("device_id", StringType()) \
    .add("temperature", DoubleType()) \
    .add("humidity", DoubleType()) \
    .add("timestamp", LongType())

# Read from Kafka
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "iot") \
    .option("startingOffsets", "latest") \
    .load()

# Convert and parse JSON
df_parsed = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Apply anomaly detection
df_with_anomaly = df_parsed.withColumn("anomaly", detect_anomaly_udf(col("temperature"), col("humidity")))

# Write to console
# Instead of console output, write to JSON files in append mode
query = df_with_anomaly.writeStream \
    .format("json") \
    .option("path", "C:/Users/geeta/spark_output") \
    .option("checkpointLocation", "C:/Users/geeta/spark-checkpoints") \
    .outputMode("append") \
    .start()

query.awaitTermination()

