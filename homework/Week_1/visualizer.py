#!/usr/bin/env python
# Name:
# Student number:
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt
import statistics

# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018

# Global dictionary for the data
data_dict = {str(key): [] for key in range(START_YEAR, END_YEAR)}

# Open file
with open(INPUT_CSV, newline = '') as csvfile:
	reader = csv.DictReader(csvfile, quoting = csv.QUOTE_NONE)
	
	# Find movie production year and append the rating to the corresponding dictionary key
	for row in reader:
		data_dict[(row['Year'])].append(float.valueof(row['Rating'])

	for key in data_dict:
		mean = float(sum(data_dict[key]) / len(data_dict[key]))

if __name__ == "__main__":
    print(data_dict)
