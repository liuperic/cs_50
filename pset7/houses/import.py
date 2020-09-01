# TODO
import csv
import cs50
from sys import argv, exit

# Check for correct number of command-line args
if len(argv) != 2:
    print('Usage: python import.py <file.csv>')
    exit(1)

# Create database by opening and closing file
open(f'students.db', 'w').close()
db = cs50.SQL("sqlite:///students.db")

# Create table and specify columns
db.execute('CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)')

# Open CSV file
with open(argv[1], mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')

    # Iterate over file
    for row in csv_reader:
        # Split full name into list containing full name
        full_name = row['name'].split()

        # Insert all data if there is a middle name
        if len(full_name) == 3:
            db.execute('INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ? ,?)',
                       full_name[0], full_name[1], full_name[2], row['house'], row['birth'])

        # Insert all data except middle name into table
        if len(full_name) == 2:
            db.execute('INSERT INTO students (first, last, house, birth) VALUES(?, ?, ?, ?)',
                       full_name[0], full_name[1], row['house'], row['birth'])
