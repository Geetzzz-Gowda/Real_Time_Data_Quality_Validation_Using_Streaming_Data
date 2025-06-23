# Real-Time Data Quality Validation Using Streaming Data

A Python-based project demonstrating real-time data quality checks on streaming data (e.g., from Kafka), using a producer-consumer model.

---

## 🔧 Features

- **Producer**: Simulates streaming data (e.g., JSON records) into a message broker.
- **Consumer**: Retrieves the streaming records and applies quality validation checks:
  - Checks for missing/duplicate/invalid field values
  - Ensures data types and value ranges
  - Flags and logs anomalies in real time

---

## ⚙️ Prerequisites

- Python 3.7+
- Kafka (or substitute with another streaming system)
- Install dependencies:

```bash
pip install -r requirements.txt
