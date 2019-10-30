import pandas as pd
import os

#Change to directory for ease of loading files
os.chdir('/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/')

########################################################################################################################
# FL_Opiate cleaning
########################################################################################################################

# FL_Opiate load
FL_Opiate = pd.read_parquet("FLopiate.parquet", engine = 'fastparquet')

# Dropped because they are not useful for the questions we are trying to answer
FL_Opiate_Droplist = ['REPORTER_ADDL_CO_INFO', 'UNIT', 'TRANSACTION_CODE',
                      'Unnamed: 0', 'REPORTER_ADDL_CO_INFO', 'REPORTER_DEA_NO',
                      'REPORTER_ADDRESS1', 'REPORTER_ADDRESS2', 'DRUG_CODE', 'Measure']

FL_Opiate = FL_Opiate.drop(FL_Opiate_Droplist, axis = 1)

# Drop Duplicates
FL_Opiate = FL_Opiate.drop_duplicates()
FL_Opiate.columns

#Drop missing County values
FL_Opiate[FL_Opiate['County'] == None]
FL_Opiate = FL_Opiate[FL_Opiate['County'] != None]

# Convert to string so can use str.extract to separate by year
FL_Opiate['TRANSACTION_DATE'] = FL_Opiate['TRANSACTION_DATE'].astype('str')

# Extract year from the string
FL_Opiate['Year'] = FL_Opiate['TRANSACTION_DATE'].str.extract('([0-9]{4}$)', expand=True)
FL_Opiate.head(5)

# Extract State from TRANSACTION_DATE -- no longer needed when we changed the file
#FL_Mort['State'] = FL_Mort['County'].str.extract('([A-Z]{2}$)', expand=True)
#FL_Mort.head(5)

#Save to Parquet file
FL_Opiate.to_parquet("FLopiate cleaned.parquet", engine = 'fastparquet')


########################################################################################################################
### FL_Mort cleaning
########################################################################################################################

FL_Mort_load = pd.read_csv("FL_mortality_2003_2015.csv")
FL_Mort_Droplist = ['Unnamed:0', 'Notes', 'County Code', 'Year Code']
FL_Mort = FL_Mort.drop_duplicates()
