# TODO
import csv
import cs50
from sys import argv, exit

# Check for correct number of command-line args
if len(argv) != 2:
    print('Usage: python roster.py <house>')
    exit(1)

# House names to look for
house_names = ['gryffindor', 'hufflepuff', 'ravenclaw', 'slytherin']

# Allow user to input house names not case sensitive
if argv[1].lower() not in house_names:
    print('Error: Invalid house name.')
    exit(2)

db = cs50.SQL("sqlite:///students.db")

# argv[1].lower().title() house input is not case-sensitive and matches db
st = db.execute('SELECT first, middle, last, birth FROM students WHERE house=? ORDER BY last, first', argv[1].lower().title())

# Iterate through query results and print out depending on whether student has middle name
for row in st:
    if row['middle']:
        print(f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")
    else:
        print(f"{row['first']} {row['last']}, born {row['birth']}")
