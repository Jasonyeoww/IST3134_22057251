import pandas as pd

# Airline code-to-name mapping
airline_map = {
    "AA": "American Airlines",
    "AS": "Alaska Airlines",
    "B6": "JetBlue Airways",
    "DL": "Delta Air Lines",
    "F9": "Frontier Airlines",
    "G4": "Allegiant Air",
    "HA": "Hawaiian Airlines",
    "NK": "Spirit Airlines",
    "UA": "United Airlines",
    "WN": "Southwest Airlines"
}

# File paths
input_file = 'Combined_Flights_2022.csv'
output_prefix = 'cleaned_chunk_'  # e.g., cleaned_chunk_0.csv

# Columns to keep
columns_to_keep = ['Cancelled', 'DepDelayMinutes', 'Marketing_Airline_Network', 'DepDel15']

chunksize = 100000

for i, chunk in enumerate(pd.read_csv(input_file, usecols=columns_to_keep, chunksize=chunksize)):
    # Drop nulls
    chunk = chunk.dropna(subset=columns_to_keep)

    # Map airline codes to names
    chunk['Airline_Name'] = chunk['Marketing_Airline_Network'].map(airline_map)

    # Drop rows where mapping failed (i.e., airlines not in the list)
    chunk = chunk.dropna(subset=['Airline_Name'])

    # Save to file
    output_file = f'{output_prefix}{i}.csv'
    chunk.to_csv(output_file, index=False)
    print(f"Saved: {output_file} | Rows: {len(chunk)}")
