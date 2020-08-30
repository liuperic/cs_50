import csv
import re
from sys import argv, exit

if len(argv) != 3:
    print('Usage: Invalid number of command-line arguments - python dna.py [file1] [file2]')
    exit(1)

with open(argv[1], mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        dna_strs = row[1:]
        break

dna_count = {}  # Create dict for dna STRs

with open(argv[2], mode='r') as file:
    for row in file:
        for seq in dna_strs:
            groups = re.findall(f'(?:{seq})+', row)
            if groups:  # If groups contain STR matches, find max
                largest = max(groups, key=len)
                dna_count[seq] = str(len(largest) // len(seq))  # Save value as string to compare to individual sequence of strings
            else:   # Else set to dna STR matches to 0
                dna_count[seq] = 0
dna_sample = list(dna_count.values())
dna_match = ''

with open(argv[1], mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        dna_strs = row[1:]
        if dna_sample == dna_strs:
            dna_match = row[0]  # Found match -> save name to dna_match

if not dna_match:
    print('No match')
else:
    print(dna_match)
