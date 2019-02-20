#!/usr/bin/env python
# Name: Daan van Lanschot
# Student number: 12486124
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt
import pandas as pd
import json

# Global constants for Input File and the 
INPUT_CSV = "input.csv"
country = "Country"
region = "Region"
population = "Pop. Density (per sq. mi.)"
infant = "Infant mortality (per 1000 births)"
gdp = "GDP ($ per capita) dollars"

def load_data(datafile):
	
	# Load data into dataframe
	datafile = pd.read_csv(datafile)
	return datafile

def select_columns(datafile, *args):
	
	# Returns datafile with only specified columns
	datafile = datafile[list(args)]
	return datafile

def remove_unknown(datafile):

	# Empty "unknown" cells, then remove incomplete data
	datafile = datafile[datafile != 'unknown']
	datafile = datafile.dropna()
	return datafile

def remove_whitespace(datafile, column):
	
	#Remove excess whitespace from specified column
	datafile[column] = datafile[column].str.strip()
	return datafile

def remove_rword(datafile, column, word):
	
	# Remove word at end, from specified column
	datafile[column] = datafile[column].str.rstrip(word)
	return datafile

def comma_point(datafile, column):

	# Replace all comma's in column with points
	datafile[column] = datafile[column].str.replace(',', '.')
	return datafile
	
def convert_numeric(datafile):

	# Converts columns containing only numbers to numeric
	datafile = datafile.apply(pd.to_numeric, errors ='ignore')
	return datafile

def remove_outliers(datafile, column, q1, q2):

	datafile[column] = datafile[column][datafile[column].between(datafile[column].quantile(q1), datafile[column].quantile(q2))]
	return datafile

def central_tendency(datafile, column):
	
	# Calculate central tendency and return as list
	mean_GDP = datafile[column].mean()
	median_GDP = datafile[column].median()
	mode_GDP = datafile[column].mode()[0]
	sd_GDP = datafile[column].std()

	return [mean_GDP, median_GDP, mode_GDP, sd_GDP]

def five_number_summary(datafile, column, q1, q2):
	
	# Calculate Five Number Summary
	minimum_IM = datafile[column].min()
	FQ_IM = datafile[column].quantile(q1)
	median_IM = datafile[column].median()
	TQ_IM = datafile[column].quantile(q2)
	maximum_IM = datafile[column].max()

	return [minimum_IM, FQ_IM, median_IM, TQ_IM, maximum_IM]

def plot_graph(datafile, column, type):
	
	# Create graph from column and show
	if type == 'hist':
		graph = datafile[column].plot.hist()
	elif type == 'box':
		graph = datafile[column].plot.box()
	else:
		return
	
	plt.show()

def save_json(datafile, index_column, path):
	datafile = datafile.set_index(index_column)
	datafile.to_json(path, orient = 'index')

if __name__ == "__main__":

	# Load dataset into dataframe
	data_pd = load_data(INPUT_CSV)
	
	# Select columns
	data_pd_columns = select_columns(data_pd, country, region, population, infant, gdp)

	# Cleaning process!
	# Remove unknown values and then clear rows with empty values
	data_pd_clean = remove_unknown(data_pd_columns)
	# Remove whitespace from columns where it is necessary
	data_pd_clean = remove_whitespace(data_pd_clean, region)
	# Remove word " dollar" from column GDP
	data_pd_clean = remove_rword(data_pd_clean, gdp, " dollars")
	# Switch comma's to points
	data_pd_clean = comma_point(data_pd_clean, population)
	data_pd_clean = comma_point(data_pd_clean, infant)
	# Turn numeric columns to numeric
	data_pd_clean = convert_numeric(data_pd_clean)
	# Remove outliers
	data_pd_clean = remove_outliers(data_pd_clean, population, 0.01, 0.99)
	data_pd_clean = remove_outliers(data_pd_clean, infant, 0.01, 0.99)
	data_pd_clean = remove_outliers(data_pd_clean, gdp, 0.01, 0.99)
	data_pd_clean = remove_unknown(data_pd_clean)

	# Calculate and print Central Tendency for GDP column
	GDP_CT = central_tendency(data_pd_clean, gdp)
	print("\n GDP Central Tendency\n GDP Mean:", GDP_CT[0], "\n GDP Median:", GDP_CT[1], "\n GDP Mode:", GDP_CT[2], "\n GDP SD:", GDP_CT[3])

	# Calculate and print Five Number Summary for Infant Mortality column
	IM_FNS = five_number_summary(data_pd_clean, infant, 0.25, 0.75)
	print("\n Infant Mortality Five Number Summary\n IM Min:", IM_FNS[0], "\n IM FQ:", IM_FNS[1], "\n IM Median:", IM_FNS[2], "\n IM TQ:", IM_FNS[3], "\n IM Max:", IM_FNS[4])

	# Print histogram for GDP and boxplot for Infant Mortality
	plot_graph(data_pd_clean, gdp, "hist")
	plot_graph(data_pd_clean, infant, "box")

	# Store processed dataframe in JSON file
	save_json(data_pd_clean, country, r'C:\Programmeren\DataProcessing\Homework\Week_2\output.json')
