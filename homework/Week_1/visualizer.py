#!/usr/bin/env python
# Name: Daan van Lanschot
# Student number: 12486124
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
		data_dict[(row['Year'])].append(float(row['Rating']))

	# Convert to average scores
	for year in data_dict:
		mean_rating = float(sum(data_dict[year]) / len(data_dict[year]))
		data_dict[year] = mean_rating

if __name__ == "__main__":
	plt.axis([-1, 10, 5, 10])
	plt.ylabel('Average Rating')
	plt.xlabel('Year of Release')
	plt.plot(*zip(*sorted(data_dict.items())), 'bo')
	plt.show()
