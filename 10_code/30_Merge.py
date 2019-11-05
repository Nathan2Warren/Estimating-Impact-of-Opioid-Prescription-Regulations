import pandas as pd
import os

os.chdir('/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/')

# To show all columns when using head or sample
pd.set_option('display.max_columns', None)

# Read Files
FL_Mort_load = pd.read_csv("20_FL_Mort cleaned.csv")
FL_Opiate_load = pd.read_parquet("FLopiate cleaned.parquet", engine = 'fastparquet')

# Do this so don't have to make reload from parquet when working
FL_Mort = FL_Mort_load.copy()
FL_Opiate = FL_Opiate_load.copy()
FL_Mort.head()
FL_Opiate.head()

########################################################################################################################
# GROUPBY
########################################################################################################################
# Rename so that we can merge easily on these columns
FL_Opiate['State'] = FL_Opiate['State'].astype(str)
FL_Opiate['Year'] = FL_Opiate['Year'].astype(str)
FL_Opiate['County'] = FL_Opiate['County'].astype(str)

FL_Opiate_Grouped = FL_Opiate.groupby(['County', 'Year', 'State']).sum().reset_index()
FL_Opiate_Grouped.shape
FL_Opiate_Grouped.head(20)

# Change types to strings so we can edit
FL_Mort['County'] = FL_Mort['County'].astype(str)
FL_Mort['Year'] = FL_Mort['Year'].astype(str)
FL_Mort['State'] = FL_Mort['State'].astype(str)

########################################################################################################################
# Merging
########################################################################################################################

#These match so that isnt the problem
FL_Mort['State'].unique()
FL_Opiate['State'].unique()

# Big Difference in the amount of counties in each and the spelling & abbreviations used
sorted(FL_Mort['County'].unique())
sorted(FL_Opiate_Grouped['County'].unique())

# Dropping Counties that are not in opiate for mort
FL_Opiate_County_Unique = FL_Opiate_Grouped['County'].unique()
FL_Opiate_County_Unique

FL_Mort_County_Unique = FL_Mort['County'].unique()
FL_Mort_County_Unique

#Look at similarities and differences to see if we missed anything
Intersection = set(FL_Mort_County_Unique).intersection(FL_Opiate_County_Unique)
Differences = set(FL_Mort_County_Unique).symmetric_difference(FL_Opiate_County_Unique)

FL_Mort = FL_Mort[FL_Mort['County'].isin(Intersection)]
FL_Opiate_Grouped = FL_Opiate_Grouped[FL_Opiate_Grouped['County'].isin(Intersection)]

# Merge
FL_Merge = pd.merge(FL_Mort, FL_Opiate_Grouped, how = 'outer', on = ['County', 'Year', 'State'], indicator = True)

########################################################################################################################
# Troubleshooting
########################################################################################################################

# Check if it worked
FL_Merge['_merge'].unique

# Look to see what is different
FL_Merge[FL_Merge['_merge'] == 'both']

# FL_Mort
FL_Merge_Left = FL_Merge[FL_Merge['_merge'] == 'left_only']
FL_Merge_Left

# Missing years for all below, have not checked all yet
FL_Opiate_Grouped[FL_Opiate_Grouped['County'] == 'ALACHUA']
FL_Mort[FL_Mort['County'] == 'ALACHUA']

FL_Opiate_Grouped[FL_Opiate_Grouped['County'] == 'BAY']
FL_Mort[FL_Mort['County'] == 'BAY']

FL_Opiate_Grouped[FL_Opiate_Grouped['County'] == 'CHARLOTTE']
FL_Mort[FL_Mort['County'] == 'CHARLOTTE']

FL_Opiate_Grouped[FL_Opiate_Grouped['County'] == 'COLUMBIA']
FL_Mort[FL_Mort['County'] == 'COLUMBIA']

FL_Opiate_Grouped[FL_Opiate_Grouped['County'] == 'FLAGLER']
FL_Mort[FL_Mort['County'] == 'FLAGLER']

FL_Opiate_Grouped[FL_Opiate_Grouped['County'] == 'HIGHLANDS']
FL_Mort[FL_Mort['County'] == 'HIGHLANDS']

# FL_Opiate
FL_Merge_Right = FL_Merge[FL_Merge['_merge'] == 'right_only']
FL_Merge_Right.shape
FL_Merge_Right

FL_Merge_Left['County'].unique()
FL_Merge_Right['County'].unique()
