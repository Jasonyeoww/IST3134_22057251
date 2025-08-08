import glob

chunk_files = sorted(glob.glob('cleaned_chunk_*.csv'))
output_file = 'all_cleaned_flights.csv'

with open(output_file, 'w', encoding='utf-8') as outfile:
    for i, filename in enumerate(chunk_files):
        with open(filename, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
            if i == 0:
                outfile.writelines(lines)  # write header + data
            else:
                outfile.writelines(lines[1:])  # skip header

print(sum(1 for _ in open('all_cleaned_flights.csv')) - 1)