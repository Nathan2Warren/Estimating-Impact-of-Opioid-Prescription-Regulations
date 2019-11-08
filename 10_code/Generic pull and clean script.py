import pandas as pd
import numpy as np

### Inputs for pulling information ###
state = 'WA'

### Functions ###
def subseter (x):
    search1 = state
    search2 = "Drug poisonings"

    state_select = x["County"].str.endswith(search1, na=False)
    x = x[state_select]
    drug_select = x["Drug/Alcohol Induced Cause"].str.startswith(search2, na=False)
    return x[drug_select]

### Loading data in ###
iter_csv = pd.read_csv("C:/Users/abhis/Documents/Duke University/IDS 690 Practical Data Science/arcos_all_washpost.tsv",
iterator=True, chunksize=500000, sep = '\t')
Opioid = pd.concat(   [chunk[chunk['BUYER_STATE']  == state] for chunk in iter_csv]   )

Mortality = pd.read_csv("C:/Users/abhis/Documents/Duke University/IDS 690 Practical Data Science/Mortality_Full.csv")
Mortality = subseter(Mortality)

### Load data sets in, if you want to skip previous steps ###
#Opioid = pd.read_csv("C:/Users/abhis/Documents/Duke University/IDS 690 Practical Data Science/WA_Opioid_data.csv")
#Mortality = pd.read_csv("C:/Users/abhis/Documents/Duke University/IDS 690 Practical Data Science/WA_Mortality_Full.csv")

### Looking at shapes ###
Opioid.shape
Mortality.shape

### Selecting columns ###
Opioid = Opioid[['BUYER_COUNTY','DRUG_NAME', 'QUANTITY', 'TRANSACTION_DATE',
                       'CALC_BASE_WT_IN_GM', 'DOSAGE_UNIT', 'Ingredient_Name',
                       'MME_Conversion_Factor','dos_str', 'Revised_Company_Name'
                       ,'BUYER_STATE']]

###  Extract year from the TRANSACTION_DATE string ###
Opioid['TRANSACTION_DATE'] = Opioid['TRANSACTION_DATE'].astype('str')
Opioid['Year'] = Opioid['TRANSACTION_DATE'].str.extract('([0-9]{4}$)', expand=True)

# Rename so we can merge later
Opioid.rename(columns = {'BUYER_STATE':'State'}, inplace = True)
Opioid.rename(columns = {'BUYER_COUNTY':'County'}, inplace = True)

### Creating MME no. ###
Opioid['MME'] = Opioid.CALC_BASE_WT_IN_GM * Opioid.MME_Conversion_Factor
Opioid = Opioid.copy()

### Recasting vars ###
Opioid['State'] = Opioid['State'].astype(str)
Opioid['Year'] = Opioid['Year'].astype(str)
Opioid['County'] = Opioid['County'].astype(str)

Mortality['County'] = Mortality['County'].astype(str)
Mortality['Year'] = Mortality['Year'].astype(str)
Mortality['Year'] = Mortality['Year'].str.rstrip('.0')
Mortality[['County','State']] = Mortality.County.str.split(', ',expand = True)
Mortality['State'] = Mortality['State'].astype(str)
Mortality['Deaths'] = Mortality['Deaths'].str.rstrip('.0')
Mortality['Deaths'] = Mortality['Deaths'].astype(int)

### Data cleaning ###
Mortality['County'] = Mortality['County'].str.rstrip(' County')
Mortality['County'] = Mortality['County'].str.upper()

### Aggregating Opioid data & Mortality do for mortality ###
Opioid = Opioid.groupby(['County', 'Year', 'State']).sum().reset_index()
Opioid = Opioid.drop(columns = ['CALC_BASE_WT_IN_GM', 'DOSAGE_UNIT', 'MME_Conversion_Factor', 'dos_str'])
Opioid.drop_duplicates()

Mortality = Mortality.groupby(['County', 'Year', 'State']).sum().reset_index()
Mortality = Mortality.drop(columns = ['Unnamed: 0', 'County Code', 'Year Code'])
Mortality = Mortality.drop_duplicates()

### Copy and paste into excel and identify the misnamed Mortality Counties, use vlookup ###
sorted(Mortality['County'].unique())
sorted(Opioid['County'].unique())

### Replaceing misnamed counties ###
d = {"BE": "BENTON", "CHELA":"CHELAN", "GRA":"GRANT", "MAS":"MASON", "THURS":"THURSTON", "SKAGI":"SKAGIT"}
Mortality["County"] = Mortality["County"].replace(d)
### REMOVE ANY COUNTIES THAT YOU CANNOT FIND A REPLACEMENT !!! ###

### Merging Mortality and Opioid ###
Combine =  pd.merge(Opioid, Mortality, how = 'left', on = ['County', 'Year', 'State'], validate = '1:1')
