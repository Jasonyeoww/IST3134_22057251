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

###  8️⃣ Sample Output
```python
+-------------------+-------------+---------------+----------------+
|Airline_Name       |total_flights|delayed_flights|delay_percentage|
+-------------------+-------------+---------------+----------------+
|Frontier Airlines  |68412        |14243          |20.82           |
|American Airlines  |249220       |53206          |21.36           |
|United Airlines    |236739       |50900          |21.50           |
+-------------------+-------------+---------------+----------------+
```
