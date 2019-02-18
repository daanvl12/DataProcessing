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

# Remove outliers
data_pd_clean["Pop. Density (per sq. mi.)"] = data_pd_clean["Pop. Density (per sq. mi.)"][data_pd_clean["Pop. Density (per sq. mi.)"].between(data_pd_clean["Pop. Density (per sq. mi.)"].quantile(.01), data_pd_clean["Pop. Density (per sq. mi.)"].quantile(.99))]
data_pd_clean["Infant mortality (per 1000 births)"] = data_pd_clean["Infant mortality (per 1000 births)"][data_pd_clean["Infant mortality (per 1000 births)"].between(data_pd_clean["Infant mortality (per 1000 births)"].quantile(.01), data_pd_clean["Infant mortality (per 1000 births)"].quantile(.99))]
data_pd_clean["GDP ($ per capita) dollars"] = data_pd_clean["GDP ($ per capita) dollars"][data_pd_clean["GDP ($ per capita) dollars"].between(data_pd_clean["GDP ($ per capita) dollars"].quantile(.01), data_pd_clean["GDP ($ per capita) dollars"].quantile(.99))]
data_pd_clean = data_pd_clean.dropna()

print(data_pd_clean)

# Plot the data
ax = plt.gca()
data_pd_clean.plot(kind = 'scatter', x = 'Pop. Density (per sq. mi.)', y = "Infant mortality (per 1000 births)", ax = ax)
#data_pd_clean.plot(kind ='line', x = 'Country', y = 'Infant mortality (per 1000 births)', color = 'red', ax = ax)
plt.show()
