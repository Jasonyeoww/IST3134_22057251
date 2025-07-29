# IST3134_22057251

# US Airline On-Time Performance Analysis using Hadoop MapReduce

This project ranks domestic airlines based on their departure punctuality using a large dataset (2018–2022).

## Files
- `mapper.py`: Mapper script for Hadoop Streaming
- `reducer.py`: Reducer script for Hadoop Streaming

## Dataset
Due to GitHub’s 25MB limit, the dataset is hosted externally:

🔗 [Download the dataset from Dropbox](https://www.dropbox.com/s/abc123/all_cleaned_flights.csv?dl=1)

Upload it to HDFS using:
```bash
wget "https://www.dropbox.com/s/abc123/all_cleaned_flights.csv?dl=1" -O all_cleaned_flights.csv
