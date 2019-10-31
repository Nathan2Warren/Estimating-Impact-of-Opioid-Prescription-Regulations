import pandas as pd
import os

#Change to directory for ease of loading files
os.chdir('/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/')
pd.set_option('display.max_columns', None)
########################################################################################################################
# FL_Opiate cleaning
########################################################################################################################

# FL_Opiate load
FL_Opiate = pd.read_parquet("FLopiate.parquet", engine = 'fastparquet')

# Drop Duplicates - there are no duplicates
#FL_Opiate.shape
#FL_Opiate = FL_Opiate.drop_duplicates()
#FL_Opiate.shape

# Only Columns we needed, When we extract the data for other states we should only open these columns (maybe less)
FL_Opiate = FL_Opiate[['BUYER_COUNTY','DRUG_NAME', 'QUANTITY', 'TRANSACTION_DATE',
                       'CALC_BASE_WT_IN_GM', 'DOSAGE_UNIT', 'Ingredient_Name',
                       'MME_Conversion_Factor','dos_str', 'Revised_Company_Name'
                       ,'BUYER_STATE']]

# Extract State from BUYER_COUNTY -- no longer needed when we changed the file
#FL_Mort['State'] = FL_Mort['County'].str.extract('([A-Z]{2}$)', expand=True)
#FL_Mort.head(5)

# Extract year from the TRANSACTION_DATE string
FL_Opiate['TRANSACTION_DATE'] = FL_Opiate['TRANSACTION_DATE'].astype('str')
FL_Opiate['Year'] = FL_Opiate['TRANSACTION_DATE'].str.extract('([0-9]{4}$)', expand=True)
FL_Opiate.head(5)

# Rename so we can merge later
FL_Opiate.rename(columns = {'BUYER_STATE':'State'}, inplace = True)
FL_Opiate.rename(columns = {'BUYER_COUNTY':'County'}, inplace = True)
FL_Opiate.head()

# Get MME and drop columns that are no longer needed
FL_Opiate['MME'] = FL_Opiate.DOSAGE_UNIT * FL_Opiate.MME_Conversion_Factor
FL_Opiate.drop(['DOSAGE_UNIT', 'MME_Conversion_Factor'], axis=1, inplace=True)
FL_Opiate.head()

# Drop missing County values
FL_Opiate[FL_Opiate['County'] == None]
FL_Opiate = FL_Opiate[FL_Opiate['County'] != None]

# Save to Parquet file
FL_Opiate.to_parquet("FLopiate cleaned.parquet", engine = 'fastparquet')


########################################################################################################################
### FL_Mort cleaning
########################################################################################################################

#Load and Drop useless columns
FL_Mort = pd.read_csv("FL_mortality_2003_2015.csv")
FL_Mort_Droplist = ['Unnamed: 0', 'Notes', 'County Code', 'Year Code']
FL_Mort.head(5)
FL_Mort = FL_Mort.drop(FL_Mort_Droplist, axis = 1)

# Change from lower case to upper case so that the merged values in 'County' will match
FL_Mort['County'] = FL_Mort['County'].str.upper()
FL_Mort['County'] = FL_Mort['County'].str.rstrip(' COUNTY')

# Make a replace dictionary fix the different naming
Replace_list = ['WAL', 'LE', 'ST.JOHNS', 'ST. LUCIE', 'BA', 'CLA', 'LEV', 'MARI', 'MARTI', 'NASSA', 'PAS']
Replace_fixed = ['WALTON', 'LEE', 'SAINT JOHNS', 'SAINT LUCIE', 'BAY', 'CLAY', 'LEVY', 'MARION', 'MARTIN', 'NASSAU', 'PASCO']
Replace_dict = dict(zip(Replace_list, Replace_fixed))

#Replace Counties with proper names
FL_Mort['County'].replace(Replace_dict, inplace = True)

#Drop Years beyond 2012 from Mort
FL_Mort['Year'] = FL_Mort['Year'].astype(int)
FL_Mort = FL_Mort[FL_Mort['Year'] < 2013]
FL_Mort['Year'] = FL_Mort['Year'].astype(str)

FL_Mort.shape

FL_Mort.to_csv("20_FL_Mort cleaned.csv")
