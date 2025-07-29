# 🛫 US Airline On-Time Performance: A Comparison of Hadoop MapReduce and Spark Approaches

This project analyzes and ranks U.S. domestic airlines based on their on-time departure performance using historical flight data from 2022. The analysis is conducted using two approaches: a Hadoop MapReduce pipeline (via Hadoop Streaming on AWS EC2) and a non-MapReduce method using Apache Spark. The goal is to compare both methods in terms of implementation and output while processing millions of flight records.

---

## 📁 Files in this Repo

- `mapper.py`: Python mapper script
- `reducer.py`: Python reducer script
- `README.md`: Project overview and full execution instructions

---

## 📦 Dataset

Due to GitHub's 25MB file limit, the cleaned dataset is hosted on Dropbox:

🔗 [Download all_cleaned_flights.csv (Dropbox)](https://www.dropbox.com/scl/fi/eqs9azgjepvb96tqua60q/all_cleaned_flights.csv?rlkey=kmhvlm4duc5k1req4vhqxk6hf&st=ypt0k7fn&dl=1)

---

## 🪜 Full Execution Guide (Hadoop MapReduce Approach)

### 1️⃣ Download the dataset on EC2

```bash
cd ~
wget "https://www.dropbox.com/scl/fi/eqs9azgjepvb96tqua60q/all_cleaned_flights.csv?rlkey=kmhvlm4duc5k1req4vhqxk6hf&st=ypt0k7fn&dl=1" -O all_cleaned_flights.csv
```

### 2️⃣ Upload to HDFS
```bash
hdfs dfs -rm -r /user/hadoop/flightdata
hdfs dfs -mkdir -p /user/hadoop/flightdata
hdfs dfs -put all_cleaned_flights.csv /user/hadoop/flightdata/
```

### 3️⃣ Save the Mapper and Reducer Scripts
mapper.py
```bash
#!/usr/bin/env python3
import sys
import csv

reader = csv.reader(sys.stdin)
for row in reader:
    try:
        if row[0] == "Cancelled":
            continue
        cancelled = row[0].strip().lower() == "true"
        delay_flag = float(row[3]) >= 1.0
        airline_name = row[4].strip()
        if not cancelled:
            print(f"{airline_name}\t1\t{int(delay_flag)}")
    except:
        continue
```
reducer.py
```bash
#!/usr/bin/env python3
import sys

current_airline = None
total_flights = 0
total_delayed = 0

for line in sys.stdin:
    line = line.strip()
    airline, flight, delay = line.split("\t")
    flight = int(flight)
    delay = int(delay)

    if current_airline and airline != current_airline:
        delay_rate = (total_delayed / total_flights) * 100
        print(f'"{current_airline}"\t{total_flights}\t{total_delayed}\t{delay_rate:.2f}')
        total_flights = 0
        total_delayed = 0

    current_airline = airline
    total_flights += flight
    total_delayed += delay

if current_airline:
    delay_rate = (total_delayed / total_flights) * 100
    print(f'"{current_airline}"\t{total_flights}\t{total_delayed}\t{delay_rate:.2f}')
```
Make them executable:
```bash
chmod +x mapper.py reducer.py
```
### 4️⃣ Run the Hadoop Streaming Job
Remove any old output:
```bash
hdfs dfs -rm -r /user/hadoop/output_ontime
```
Then run the job:
```bash
hadoop jar /home/hadoop/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input /user/hadoop/flightdata/all_cleaned_flights.csv \
  -output /user/hadoop/output_ontime \
  -mapper ./mapper.py \
  -reducer ./reducer.py \
  -file mapper.py \
  -file reducer.py
```

### 5️⃣ View the Final Results (Sorted)
```bash
hdfs dfs -cat /user/hadoop/output_ontime/part-00000 | sort -t $'\t' -k4 -n
```
---

## 🪜 Full Execution Guide (Apache Spark Approach)

### 1️⃣ Import Required Libraries
```bash
from pyspark.sql.functions import col, when, count, sum as spark_sum, round
```

### 2️⃣ Load Dataset from HDFS
```bash
df = spark.read.csv("hdfs:///user/hadoop/flightdata/all_cleaned_flights.csv", header=True, inferSchema=True)
```

### 3️⃣ Filter Out Cancelled Flights
```bash
df_filtered = df.filter(col("Cancelled") != 1)
```

### 4️⃣ Create Delay Flag Column
```bash
df_flagged = df_filtered.withColumn("delay_flag", when(col("DepDel15") == 1, 1).otherwise(0))
```

### 5️⃣ Aggregate Delay Stats by Airline
```bash
agg_df = df_flagged.groupBy("Airline_Name").agg(
    count("*").alias("total_flights"),
    spark_sum("delay_flag").alias("delayed_flights")
)
```

### 6️⃣ Calculate Delay Percentage and Sort
```bash
final_df = agg_df.withColumn("delay_percentage",
                             round((col("delayed_flights") / col("total_flights")) * 100, 2)) \
                 .orderBy("delay_percentage")
```

### 7️⃣ Show Final Results
```bash
final_df.select("Airline_Name", "total_flights", "delayed_flights", "delay_percentage") \
    .show(truncate=False)
```
