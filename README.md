# 🛫 US Airline On-Time Performance: A Comparison of Hadoop MapReduce and Spark Approaches

This project analyzes and ranks U.S. domestic airlines based on their on-time departure performance using historical flight data from 2022. The analysis is conducted using two approaches: a Hadoop MapReduce pipeline (via Hadoop Streaming on AWS EC2) and a non-MapReduce method using Apache Spark. The goal is to compare both methods in terms of implementation and output while processing millions of flight records.

---

## 📁 Files in this Repo

- `README.md`: Project overview
- `01_preprocess_chunks.py`: Script to clean and split the raw Kaggle dataset into chunks
- `02_merge_chunks.py`: Script to merge cleaned chunks into a single CSV file
- `MapReduce Approach.md`: Full execution guide and explanation of the Hadoop MapReduce implementation
- `Non-MapReduce Approach.md`: Full execution guide and explanation of the Apache Spark (non-MapReduce) implementation

---

## 📦 Dataset

This project uses flight performance data sourced from Kaggle:

🔗 [Flight Delay Dataset 2018–2022 (Kaggle)](https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022?select=Combined_Flights_2022.csv)

- **Original File Name**: `Combined_Flights_2022.csv`
- **File Size**: ~1.42 GB
- **Total Records**: ~4.08 million rows

Due to GitHub's 25MB file size limit, the cleaned dataset used in this project has been hosted externally:

🔗 [Download `all_cleaned_flights.csv` (Dropbox)](https://www.dropbox.com/scl/fi/eqs9azgjepvb96tqua60q/all_cleaned_flights.csv?rlkey=kmhvlm4duc5k1req4vhqxk6hf&st=ypt0k7fn&dl=1)

The cleaned version contains only the relevant columns used for analysis (e.g., cancellation status, delay indicator, airline name).


---


## 🧹 Data Preprocessing Scripts

To generate the cleaned dataset (`all_cleaned_flights.csv`), we used the following Python scripts:

1. **`01_preprocess_chunks.py`**  
   - Reads the raw Kaggle file (`Combined_Flights_2022.csv`)
   - Keeps relevant columns only: `Cancelled`, `DepDelayMinutes`, `Marketing_Airline_Network`, `DepDel15`
   - Maps airline codes to full names
   - Splits into chunks (100,000 rows per file) and drops rows with missing or unmapped values

2. **`02_merge_chunks.py`**  
   - Merges all chunked CSVs (`cleaned_chunk_*.csv`) into one final cleaned dataset: `all_cleaned_flights.csv`

---
## 👥 Group Members

| Name                    | Student ID  |
|-------------------------|-------------|
| Jason Yeow Jun Kit      | 22057251    |
| Joselyn Chin Shi Min    | 22049126    |
| Leong Zheng Xuan        | 21026976    |
