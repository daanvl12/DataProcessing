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

# Global constants for the input file
INPUT_CSV = "input.csv"

# Load data into dataframe
data_pd = pd.read_csv(INPUT_CSV, decimal=',')
data_pd_columns = data_pd[["Country", "Region", "Pop. Density (per sq. mi.)", "Infant mortality (per 1000 births)", "GDP ($ per capita) dollars"]]

# Empty "unknown" cells, then remove incomplete data
data_pd_clean = data_pd_columns[data_pd_columns != 'unknown']
data_pd_clean = data_pd_clean.dropna()

# Remove excess whitespace from region column
data_pd_clean["Region"] = data_pd_clean["Region"].str.strip()

# Remove word dollar from GDP list
data_pd_clean["GDP ($ per capita) dollars"] = data_pd_clean["GDP ($ per capita) dollars"].str.rstrip(' dollars')

# Convert dtype to numeric
data_pd_clean["Pop. Density (per sq. mi.)"] = data_pd_clean["Pop. Density (per sq. mi.)"].str.replace(',', '.')
data_pd_clean = data_pd_clean.apply(pd.to_numeric, errors ='ignore')

print(data_pd_clean.dtypes)

# Plot the data
ax = plt.gca()
data_pd_clean.plot(kind = 'scatter', x = 'Infant mortality (per 1000 births)', y = 'GDP ($ per capita) dollars', ax = ax)
#data_pd_clean.plot(kind ='line', x = 'Country', y = 'Infant mortality (per 1000 births)', color = 'red', ax = ax)
plt.show()
