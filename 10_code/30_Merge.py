import pandas as pd
import os

os.setcwd('')

# To show all columns when using head or sample
pd.set_option('display.max_columns', None)

# Read Files
FL_Mort_load = pd.read_csv("/Users/N1/690 local/FL_mortality_2003_2015.csv")
FL_Opiate_load = pd.read_parquet("/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/FLopiate.parquet", engine = 'fastparquet')

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
FL_Merge[FL_Merge['_merge'] == 'left_only']

# FL_Opiate
FL_Merge[FL_Merge['_merge'] == 'right_only']
# We have a bunch of Counties that equal none
FL_Opiate[FL_Opiate['County'] == None]
FL_Opiate[FL_Opiate['County'] == 'SEMINOLE']
FL_Mort[FL_Mort['County'] == 'SEMINOLE']

#Something is wrong with one of the keys since all the years, County name and State match
FL_Opiate_Test[FL_Opiate_Test['County'] == 'SEMINOLE']
FL_Mort_Test[FL_Mort_Test['County'] == 'SEMINOLE']
