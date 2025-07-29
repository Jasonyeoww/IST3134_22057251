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