import pandas as pd
import numpy as np
import glob
from plotnine import *
import os
os.chdir('C:/Users/Jiajie Zhang/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files')
os.getcwd()
# combine data in all files
appended_data = pd.DataFrame()
for filename in glob.glob('C:/Users/Jiajie Zhang/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/US_VitalStatistics/*.txt'):
    df_tmp = pd.read_csv(filename, sep='\t')
    appended_data = appended_data.append(df_tmp)

def subseter (x):
    search2 = "Drug poisonings"
    Y = x["Drug/Alcohol Induced Cause"].str.startswith(search2, na=False)
    return x[Y]

State_data = subseter(appended_data)
for i in State_data['Deaths'].value_counts().index:
    print(i)

(State_data['Deaths'] == 'Missing').sum()

State_data.loc[State_data['Deaths'] == 'Missing']
State_data['Deaths'].replace({'Missing':0},inplace = True)


State_data.drop(columns = ['Year Code','Notes','Drug/Alcohol Induced Cause','Drug/Alcohol Induced Cause Code'],inplace = True)

# expand county state to two columns
State_data[['County', 'State']] = State_data['County'].str.split(', ', expand=True)
State_data.loc[:,'County'].str.replace(' County','')
##convert datatypes
State_data[['County Code','Year']]= State_data[['County Code','Year']].astype('int')
State_data['Deaths'] = State_data['Deaths'].astype('int')
State_data.loc[:,'County'].str.upper()
State_data.drop_duplicates(inplace = True)
State_data.dtypes
State_data.to_csv('15_Drug_Mortality_Full.csv')
