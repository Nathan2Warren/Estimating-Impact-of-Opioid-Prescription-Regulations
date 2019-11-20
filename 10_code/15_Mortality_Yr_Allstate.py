import glob
import pandas as pd
import zipfile
import numpy as np
from plotnine import *
import matplotlib as mpl
import os

# Make it easy to use for everyone
os.chdir("/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/US_VitalStatistics")

appended_data = pd.DataFrame()
for filename in glob.glob('*.txt'):
    df_tmp = pd.read_csv(filename, sep='\t')
    appended_data = appended_data.append(df_tmp)
# Split county and State
appended_data[['County', 'State']] = appended_data.County.str.split(', ', expand=True)
# Drop nan data(last few columns)
appended_data_dropna = appended_data.dropna(thresh=5)

# Subset function select only drug poisoning induced deaths.


def subseter(x):
    search2 = "Drug poisonings"
    Y = x["Drug/Alcohol Induced Cause"].str.startswith(search2, na=False)
    return x[Y]


Drug_mortality_allstate = subseter(appended_data_dropna)
Drug_mortality_allstate['Drug/Alcohol Induced Cause Code'].value_counts()

# Replace 'Missing' string in 'Deaths' column
Drug_mortality_allstate['Deaths'] = Drug_mortality_allstate['Deaths'].replace('Missing', np.nan)

# Convert types in 'Deaths' all to float
Drug_mortality_allstate['Deaths'] = Drug_mortality_allstate['Deaths'].astype('float64', copy=False)

# Not required
sort = Drug_mortality_allstate.sort_values(by='Deaths')

# Group data by Year and State
Grouped = Drug_mortality_allstate.groupby(['State', 'Year'], as_index=False)['Deaths'].sum()
Grouped.to_csv("/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files/15_Grouped_Population_Death_Data.csv")
