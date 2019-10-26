import pandas as pd
import re

# To show all columns when using head or sample
pd.set_option('display.max_columns', None)

# Read Files
FL_Mort = pd.read_csv("/Users/N1/690 local/FL_mortality_2003_2015.csv")
FL_Opiate = pd.read_parquet("/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/FLopiate.parquet", engine = 'fastparquet')

FL_Mort.sample(5)
FL_Opiate.sample(5)

# Dropped because they don't add anything
FL_Opiate = FL_Opiate.drop('REPORTER_ADDL_CO_INFO', axis = 1)
FL_Opiate = FL_Opiate.drop('UNIT', axis = 1)
FL_Opiate['TRANSACTION_CODE'].unique
FL_Opiate = FL_Opiate.drop('TRANSACTION_CODE', axis = 1)

# Convert to string so can use str.endswith to separate by year
FL_Opiate['TRANSACTION_DATE'] = FL_Opiate['TRANSACTION_DATE'].astype('str')

# Extract year from the string
FL_Opiate['Year'] = FL_Opiate['TRANSACTION_DATE'].str.extract('([0-9]{4}$)', expand=True)
FL_Mort['State'] = FL_Mort['County'].str.extract('([A-Z]{2}$)', expand=True)
FL_Mort.head(5)

# Rename so that we can merge easily on these columns
FL_Opiate.rename(columns = {'BUYER_STATE':'State'}, inplace = True)
FL_Opiate.rename(columns = {'BUYER_COUNTY':'County'}, inplace = True)

# Change types to strings so we can merge on them
FL_Mort['County'] = FL_Mort['County'].astype(str)
FL_Mort['Year'] = FL_Mort['Year'].astype(str)
FL_Mort['State'] = FL_Mort['State'].astype(str)

FL_Opiate['State'] = FL_Opiate['State'].astype(str)
FL_Opiate['Year'] = FL_Opiate['Year'].astype(str)
FL_Opiate['County'] = FL_Opiate['County'].astype(str)

# Change from uppercase to lower case so that the merged values in 'County' will match
FL_Mort['County'] = FL_Mort['County'].str.upper()

# Stringsplit so to remove County from the end of counties
FL_Mort[['County', 'County1']] = FL_Mort['County'] .str.split(' COUNTY', expand = True)
# Drop the resulting blank column
FL_Mort['County1'].drop

#Merge (we should take out state since it is already all Florida)
FL_Merge = pd.merge(FL_Mort, FL_Opiate, how = 'outer', on = ['County', 'Year', 'State'], indicator = True)

#Check if it worked
FL_Merge['_merge'].unique
