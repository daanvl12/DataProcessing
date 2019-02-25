# Name: Daan van Lanschot
# Student number: 12486124
"""
This script visualizes data obtained from the KNMI
"""

import numpy as np
import pandas as pd

# Global Variables
INPUT_TXT = "KNMI_20181231.txt"

def load_txt(datafile):
	datafile = np.loadtxt(datafile, delimiter=',')
	return datafile

def convert_dataframe(datafile, *args):
	arguments = list(args)
	dataframe = pd.DataFrame(data = datafile, columns = arguments)
	return dataframe

def drop_column(datafile, column):
	datafile = datafile.drop(column, axis=1)
	return datafile

def convert_datetime(datafile, column):
	datafile[column] = datafile[column].astype(str)
	datafile[column] = datafile[column].str.partition('.')
	return datafile

def divide_column(datafile, column):
	datafile[column] = datafile[column] / 10
	return datafile

def save_json(datafile, index_column, path):
	datafile = datafile.set_index(index_column)
	datafile.to_json(path, orient = 'index')

if __name__ == "__main__":

	# Load data
	textfile = load_txt(INPUT_TXT)

	# Convert to pandas dataframe
	data_pd = convert_dataframe(textfile, 'Location', 'Date', 'Temperature')

	# Drop location column
	data_pd = drop_column(data_pd, 'Location')

	# Convert date column to actual date notation
	data_pd = convert_datetime(data_pd, 'Date')
	
	# Convert temperature to actual temperature
	data_pd = divide_column(data_pd, 'Temperature')
	print(data_pd)

	# Save as json
	save_json(data_pd, 'Date', r'C:\Programmeren\DataProcessing\Homework\Week_3\output.json')
