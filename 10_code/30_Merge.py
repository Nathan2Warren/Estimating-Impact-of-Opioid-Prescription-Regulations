import pandas as pd
import os

os.setcwd('"/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/')

# To show all columns when using head or sample
pd.set_option('display.max_columns', None)

# Read Files
FL_Mort_load = pd.read_csv("FL_mortality_2003_2015.csv")
FL_Opiate_load = pd.read_parquet("FLopiate.parquet", engine = 'fastparquet')

FL_Mort = FL_Mort_load.copy()
FL_Opiate = FL_Opiate_load.copy()
FL_Mort.head()
FL_Opiate.head()

##### FL_Opiate Editing
# Dropped because they don't add anything
FL_Opiate = FL_Opiate.drop('REPORTER_ADDL_CO_INFO', axis = 1)
FL_Opiate = FL_Opiate.drop('UNIT', axis = 1)
FL_Opiate = FL_Opiate.drop('TRANSACTION_CODE', axis = 1)

# Convert to string so can use str.extract to separate by year
FL_Opiate['TRANSACTION_DATE'] = FL_Opiate['TRANSACTION_DATE'].astype('str')

# Extract year from the string
FL_Opiate['Year'] = FL_Opiate['TRANSACTION_DATE'].str.extract('([0-9]{4}$)', expand=True)
FL_Opiate.head(5)

# Extract State from TRANSACTION_DATE -- no longer needed when we changed the file
#FL_Mort['State'] = FL_Mort['County'].str.extract('([A-Z]{2}$)', expand=True)
#FL_Mort.head(5)

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
FL_Opiate = FL_Opiate.drop_duplicates()

FL_Mort.shape
FL_Opiate.shape

##### Creating Test for merging
FL_Mort_Test = FL_Mort[['State', 'Year', 'County']]
FL_Opiate_Test = FL_Opiate[['State', 'Year', 'County']]

# Merge (we should take out state since it is already all Florida)
FL_Merge = pd.merge(FL_Mort_Test, FL_Opiate_Test, how = 'outer', on = ['County', 'Year', 'State'], indicator = True)

# Check if it worked
FL_Merge['_merge'].unique

# Look to see what is different

FL_Merge[FL_Merge['_merge'] == 'both']

# FL_Mort
FL_Merge_Left = FL_Merge[FL_Merge['_merge'] == 'left_only']

# FL_Opiate
FL_Merge_Right = FL_Merge[FL_Merge['_merge'] == 'right_only']

FL_Merge_Left['County'].unique()
FL_Merge_Right['County'].unique()

# We have a bunch of Counties that equal none
FL_Opiate[FL_Opiate['County'] == None]
FL_Opiate[FL_Opiate['County'] == 'SEMINOLE']
FL_Mort[FL_Mort['County'] == 'SEMINOLE']

#Something is wrong with one of the keys since all the years, County name and State match
FL_Opiate_Test[FL_Opiate_Test['County'] == 'SEMINOLE']
FL_Mort_Test[FL_Mort_Test['County'] == 'SEMINOLE']

#Opiate_Test only goes till 2012 while Mort goes till 2015
FL_Mort_Test['Year'].unique()
FL_Opiate_Test['Year'].unique()

#Drop Mort beyond 2012 from Mort
FL_Mort_Test['Year'] = FL_Mort_Test['Year'].astype(int)
FL_Mort_Test = FL_Mort_Test[FL_Mort_Test['Year'] < 2013]
FL_Mort_Test['Year'] = FL_Mort_Test['Year'].astype(str)

#Drop None from Opiate
FL_Opiate_Test = FL_Opiate_Test[FL_Opiate_Test['County'] != None]
FL_Opiate_Test['Year'].unique()

#These match so that isnt the problem
FL_Mort_Test['State'].unique()
FL_Opiate_Test['State'].unique()

# FL_Opiate_Test has a lot more counties
sorted(FL_Mort_Test['County'].unique())
FL_Mort_Test['County'].replace(to_replace=['WAL'], value=['WALTON'], inplace=True)
FL_Mort_Test['County'].replace(to_replace=['LE'], value=['LEE'], inplace=True)
FL_Mort_Test['County'].replace(to_replace=['ST. JOHNS'], value=['SAINT JOHNS'], inplace=True)
FL_Mort_Test['County'].replace(to_replace=['ST. LUCIE'], value=['SAINT LUCIE'], inplace=True)
FL_Mort_Test['County'].replace(to_replace=['BA'], value=['BAY'], inplace=True)
FL_Mort_Test['County'].replace(to_replace=['CLA'], value=['CLAY'], inplace=True)
FL_Mort_Test['County'].replace(to_replace=['LEV'], value=['LEVY'], inplace=True)
FL_Mort_Test['County'].replace(to_replace=['MARI'], value=['MARION'], inplace=True)
FL_Mort_Test['County'].replace(to_replace=['MARTI'], value=['MARTIN'], inplace=True)
FL_Mort_Test['County'].replace(to_replace=['NASSA'], value=['NASSAU'], inplace=True)
FL_Mort_Test['County'].replace(to_replace=['PAS'], value=['PASCO'], inplace=True)
FL_Mort_Test['County'].replace(to_replace=['OKEECHOBEE'], value=['OKEECHOBEE'], inplace=True)
sorted(FL_Opiate_Test['County'].unique())

# Dropping Counties that do not match // NOT DONE YET
keepers = ['ALACHUA', 'BA', 'BREVARD', 'BROWARD', 'CITRUS', 'CLA', 'COLLIER',
       'DUVAL', 'ESCAMBIA', 'HERNAND', 'HIGHLANDS', 'HILLSBOROUGH',
       'INDIAN RIVER', 'LAKE', 'LEE', 'LE', 'MANATEE', 'MARI', 'MARTI',
       'MIAMI-DADE', 'MONROE', 'OKALOOSA', 'ORANGE', 'OSCEOLA',
       'PALM BEACH', 'PAS', 'PINELLAS', 'POLK', 'ST. LUCIE', 'SANTA ROSA',
       'SARASOTA', 'SEMINOLE', 'VOLUSIA', 'CHARLOTTE', 'NASSA', 'PUTNAM',
       'ST. JOHNS', 'COLUMBIA', 'WAL', 'OKEECHOBEE', 'FLAGLER', 'LEV']

FL_Opiate_Test = FL_Opiate_Test[FL_Opiate_Test['County'].isin(keepers)]
FL_Mort_Test = FL_Mort_Test[FL_Mort_Test['County'].isin(keepers)]
