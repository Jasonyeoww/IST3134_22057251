## 🪜 Full Execution Guide (Hadoop MapReduce Approach)

### 1️⃣ Dataset Preparation
The cleaned dataset all_cleaned_flights.csv was downloaded from Dropbox (preprocessed from the original Kaggle dataset):
```bash
cd ~
wget "https://www.dropbox.com/scl/fi/eqs9azgjepvb96tqua60q/all_cleaned_flights.csv?rlkey=kmhvlm4duc5k1req4vhqxk6hf&st=ypt0k7fn&dl=1" -O all_cleaned_flights.csv
```

We then uploaded the file to HDFS:
```bash
hdfs dfs -rm -r /user/hadoop/flightdata
hdfs dfs -mkdir -p /user/hadoop/flightdata
hdfs dfs -put all_cleaned_flights.csv /user/hadoop/flightdata/
```

### 2️⃣  Mapper and Reducer Scripts
Two Python scripts were written to perform the MapReduce job. The mapper emits tuples in the form:
<Airline_Name> <1> <delay_flag> — where delay_flag = 1 if the delay is ≥ 15 minutes.

#### mapper.py
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
#### reducer.py
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
Scripts were made executable using:
```bash
chmod +x mapper.py reducer.py
```
### 3️⃣ Hadoop Streaming Job Execution
The MapReduce job was executed using the Hadoop Streaming JAR:
```bash
hdfs dfs -rm -r /user/hadoop/output_ontime
hadoop jar /home/hadoop/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input /user/hadoop/flightdata/all_cleaned_flights.csv \
  -output /user/hadoop/output_ontime \
  -mapper ./mapper.py \
  -reducer ./reducer.py \
  -file mapper.py \
  -file reducer.py
```

### 4️⃣ Output & Sorting
Final output was retrieved and sorted based on delay percentage:
```bash
hdfs dfs -cat /user/hadoop/output_ontime/part-00000 | sort -t $'\t' -k4 -n
```

### 5️⃣ Sample Output
```bash
"Frontier Airlines"      68412   14243   20.82
"American Airlines"      249220  53206   21.36
"United Airlines"        236739  50900   21.50
```

---
