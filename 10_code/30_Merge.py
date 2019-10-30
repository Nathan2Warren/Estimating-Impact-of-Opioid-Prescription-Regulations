import pandas as pd
import os

os.chdir('/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/')

# To show all columns when using head or sample
pd.set_option('display.max_columns', None)

# Read Files
FL_Mort_load = pd.read_csv("FL_mortality_2003_2015.csv")
FL_Opiate_load = pd.read_parquet("FLopiate.parquet", engine = 'fastparquet')

# Do this so don't have to make reload from parquet when working
FL_Mort = FL_Mort_load.copy()
FL_Opiate = FL_Opiate_load.copy()
FL_Mort.head()
FL_Opiate.head()

##### FL_Opiate Editing

# Rename so that we can merge easily on these columns
FL_Opiate.rename(columns = {'BUYER_STATE':'State'}, inplace = True)
FL_Opiate.rename(columns = {'BUYER_COUNTY':'County'}, inplace = True)

######### FL_Mort Editing
# Change types to strings so we can edit
FL_Mort['County'] = FL_Mort['County'].astype(str)
FL_Mort['Year'] = FL_Mort['Year'].astype(str)
FL_Mort['State'] = FL_Mort['State'].astype(str)
FL_Opiate.head()
FL_Opiate['State'] = FL_Opiate['State'].astype(str)
FL_Opiate['Year'] = FL_Opiate['Year'].astype(str)
FL_Opiate['County'] = FL_Opiate['County'].astype(str)

# Change from lower case to upper case so that the merged values in 'County' will match
FL_Mort['County'] = FL_Mort['County'].str.upper()
FL_Mort['County'] = FL_Mort['County'].str.rstrip(' COUNTY')

# Drop Duplicates
FL_Mort = FL_Mort.drop_duplicates()

FL_Mort.shape
FL_Opiate.shape

##### Creating Test for merging
FL_Mort_Test = FL_Mort[['State', 'Year', 'County']]
FL_Opiate_Test = FL_Opiate[['State', 'Year', 'County']]

#Opiate_Test only goes till 2012 while Mort goes till 2015
FL_Mort_Test['Year'].unique()
FL_Opiate_Test['Year'].unique()

#Drop Mort beyond 2012 from Mort
FL_Mort_Test['Year'] = FL_Mort_Test['Year'].astype(int)
FL_Mort_Test = FL_Mort_Test[FL_Mort_Test['Year'] < 2013]
FL_Mort_Test['Year'] = FL_Mort_Test['Year'].astype(str)

#These match so that isnt the problem
FL_Mort_Test['State'].unique()
FL_Opiate_Test['State'].unique()

# Big Difference in the amount of counties in each and the spelling & abbreviations used
sorted(FL_Mort_Test['County'].unique())
sorted(FL_Opiate_Test['County'].unique())

# Make a replace dictionary fix the different naming
Replace_list = ['WAL', 'LE', 'ST.JOHNS', 'ST. LUCIE', 'BA', 'CLA', 'LEV', 'MARI', 'MARTI', 'NASSA', 'PAS']
Replace_fixed = ['WALTON', 'LEE', 'SAINT JOHNS', 'SAINT LUCIE', 'BAY', 'CLAY', 'LEVY', 'MARION', 'MARTIN', 'NASSAU', 'PASCO']
Replace_dict = dict(zip(Replace_list, Replace_fixed))

#Replace Counties
FL_Mort_Test['County'].replace(Replace_dict, inplace = True)

sorted(FL_Mort_Test['County'].unique())
sorted(FL_Opiate_Test['County'].unique())

# Dropping Counties that do not match // NOT DONE YET
keepers = ['ALACHUA', 'BAY', 'BREVARD', 'BROWARD', 'CITRUS', 'CLAY', 'COLLIER',
       'DUVAL', 'ESCAMBIA', 'HERNAND', 'HIGHLANDS', 'HILLSBOROUGH',
       'INDIAN RIVER', 'LAKE', 'LEE', 'MANATEE', 'MARI', 'MARTI',
       'MIAMI-DADE', 'MONROE', 'OKALOOSA', 'ORANGE', 'OSCEOLA',
       'PALM BEACH', 'PAS', 'PINELLAS', 'POLK', 'ST. LUCIE', 'SANTA ROSA',
       'SARASOTA', 'SEMINOLE', 'VOLUSIA', 'CHARLOTTE', 'NASSAU', 'PUTNAM',
       'SAINT JOHNS', 'COLUMBIA', 'WALTON', 'OKEECHOBEE', 'FLAGLER', 'LEV']


FL_Opiate_Test = FL_Opiate_Test[FL_Opiate_Test['County'].isin(keepers)]
FL_Mort_Test = FL_Mort_Test[FL_Mort_Test['County'].isin(keepers)]


# Merge (we should take out state since it is already all Florida)
FL_Merge = pd.merge(FL_Mort_Test, FL_Opiate_Test, how = 'outer', on = ['County', 'Year', 'State'], indicator = True)

# Check if it worked
FL_Merge['_merge'].unique

# Look to see what is different
FL_Merge[FL_Merge['_merge'] == 'both']

# FL_Mort
FL_Merge_Left = FL_Merge[FL_Merge['_merge'] == 'left_only']
FL_Merge_Left

# FL_Opiate
FL_Merge_Right = FL_Merge[FL_Merge['_merge'] == 'right_only']
FL_Merge_Right

FL_Merge_Left['County'].unique()
FL_Merge_Right['County'].unique()
