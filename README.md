# Real-Time Data Quality Validation Using Streaming Data

A Python-based project demonstrating real-time data quality checks on streaming data (e.g., from Kafka), using a producer-consumer model enhanced with machine learning-based anomaly detection and real-time visualization.

---

## Features

- **Producer**: Simulates streaming data (e.g., JSON records) into a Kafka topic.
- **Consumer**: 
  - Retrieves streaming records using PySpark Structured Streaming.
  - Applies data quality validation checks including:
    - Missing, duplicate, or invalid field values.
    - Data type enforcement and value range checks.
  - Runs ML-based anomaly detection (Isolation Forest) on sensor data.
  - Flags and logs anomalies in real time.
  - Writes processed data with anomaly flags to output files.
- **Visualization Dashboard**: Real-time monitoring of data quality and anomalies using Streamlit.

---

## Prerequisites

- Python 3.7 or higher
- Java 8 or higher (required for Apache Spark)
- Apache Kafka and Zookeeper installed and running locally
- Kafka Python client and PySpark packages
- Additional Python libraries listed in `requirements.txt`

---

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/Geetzzz-Gowda/Real_Time_Data_Quality_Validation_Using_Streaming_Data.git
   cd Real_Time_Data_Quality_Validation_Using_Streaming_Data
