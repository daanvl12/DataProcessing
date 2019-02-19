#!/usr/bin/env python
# Name: Daan van Lanschot
# Student number: 12486124
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import pandas as pd
import json

# Global constants for the input file
INPUT_CSV = "input.csv"
country = "Country"
region = "Region"
population = "Pop. Density (per sq. mi.)"
infant = "Infant mortality (per 1000 births)"
gdp = "GDP ($ per capita) dollars"

# Load data into dataframe
data_pd = pd.read_csv(INPUT_CSV, decimal=',')
data_pd_columns = data_pd[[country, region, population, infant, gdp]]

# Empty "unknown" cells, then remove incomplete data
data_pd_clean = data_pd_columns[data_pd_columns != 'unknown']
data_pd_clean = data_pd_clean.dropna()

# Remove excess whitespace from region column
data_pd_clean[region] = data_pd_clean[region].str.strip()

# Remove word dollar from GDP list
data_pd_clean[gdp] = data_pd_clean[gdp].str.rstrip(' dollars')

# Convert dtype to numeric
data_pd_clean[population] = data_pd_clean[population].str.replace(',', '.')
data_pd_clean = data_pd_clean.apply(pd.to_numeric, errors ='ignore')

# Remove outliers
data_pd_clean[population] = data_pd_clean[population][data_pd_clean[population].between(data_pd_clean[population].quantile(.01), data_pd_clean[population].quantile(.99))]
data_pd_clean[infant] = data_pd_clean[infant][data_pd_clean[infant].between(data_pd_clean[infant].quantile(.01), data_pd_clean[infant].quantile(.99))]
data_pd_clean[gdp] = data_pd_clean[gdp][data_pd_clean[gdp].between(data_pd_clean[gdp].quantile(.01), data_pd_clean[gdp].quantile(.99))]
data_pd_clean = data_pd_clean.dropna()

# Calculate different GDP values
mean_GDP = data_pd_clean[gdp].mean()
median_GDP = data_pd_clean[gdp].median()
mode_GDP = data_pd_clean[gdp].mode()[0]
sd_GDP = data_pd_clean[gdp].std()

print("\n GDP Central Tendency\n", "GDP Mean:", mean_GDP, "\n", "GDP Median:", median_GDP, "\n", "GDP Mode:", mode_GDP, "\n", "GDP SD:", sd_GDP)

# Calculate Five Number Summary
minimum_IM = data_pd_clean[infant].min()
FQ_IM = data_pd_clean[infant].quantile(0.25)
median_IM = data_pd_clean[infant].median()
TQ_IM = data_pd_clean[infant].quantile(0.75)
maximum_IM = data_pd_clean[infant].max()

print("\n Infant Mortality Five Number Summary\n", "IM Min:", minimum_IM, "\n", "IM FQ:", FQ_IM, "\n", "IM Median:", median_IM, "\n", "IM TQ:", TQ_IM, "\n", "IM Max:", maximum_IM)

# Create and display both figures
hist_GDP = data_pd_clean[gdp].plot.hist()
plt.show()
boxplot_IM = data_pd_clean[infant].plot.box()
plt.show()

# Export to JSON
data_pd_json = data_pd_clean.set_index(country)
data_pd_json.to_json(r'C:\Programmeren\DataProcessing\Homework\Week_2\output.json', orient = 'index')
