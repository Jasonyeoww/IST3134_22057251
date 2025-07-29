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