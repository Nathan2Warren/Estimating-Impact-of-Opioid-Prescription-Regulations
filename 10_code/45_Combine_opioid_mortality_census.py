import pandas as pd
import numpy as np
import glob
import os
from plotnine import *
os.chdir('C:/Users/Jiajie Zhang/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files')
os.getcwd()

#read in opioid data
Opioid_Mort = pd.DataFrame()
for filename in glob.glob('./*cleaned_and_merged.csv'):
    print(filename)
    df_tmp = pd.read_csv(filename)
    Opioid_Mort = Opioid_Mort.append(df_tmp)

Census =  pd.read_csv('21_Census_Full_County_Level.csv')

Fips = pd.read_csv('01_county_fips_master.csv',encoding='latin-1')
Fips = Fips[['fips','county_name','state_abbr']]
Fips['county_name'] = Fips['county_name'].str.replace(' County','').str.upper()
#Fips['county_name'].str.upper()
Fips['County_State'] = Fips['county_name'].map(str) + ' ' + Fips['state_abbr']

# find mismatch states
sorted(Fips['county_name'].unique().astype('str'))
sorted(Opioid_Mort['County'].unique().astype('str'))

Opioid_Mort['County_State'] = Opioid_Mort['County'].map(str) + ' ' + Opioid_Mort['State']

#merge opioid wit fips
list(sorted(Opioid_Mort_Fips.loc[Opioid_Mort_Fips['fips'].isna()]['County'].unique().astype('str')))


d= {'DE KALB IN':'DEKALB IN','DE SOTO FL':'DESOTO FL','DE WITT TX':'DEWITT TX','DEWITT IL':'DE WITT IL','LA PORTE IN':'LAPORTE IN','LA SALLE IL':'LASALLE IL','SAINT CLAIR IL':'ST. CLAIR IL','SAINT LUCIE FL':'ST. LUCIE FL','SAINT JOHNS FL':'ST. JOHNS FL','ST JOSEPH IN':'ST. JOSEPH IN'}
Opioid_Mort['County_State'] = Opioid_Mort['County_State'].replace(d)
Opioid_Mort_Fips = pd.merge(Opioid_Mort,Fips,how = 'left', left_on = ['County_State'],right_on = ['County_State'])
mismatch_state  = sorted(Opioid_Mort_Fips.loc[Opioid_Mort_Fips['fips'].isna()]['County_State'].astype('str').unique())

###

# drop county code na:
Opioid_Mort_Fips_cleaned = Opioid_Mort_Fips.drop(index = Opioid_Mort_Fips.loc[Opioid_Mort_Fips['fips'].isna()]['County_State'].index)

#convert fips into int
Opioid_Mort_Fips_cleaned['fips'] = Opioid_Mort_Fips_cleaned['fips'].astype('int')

#replace county name sin Opioid_Mort

#merge Opioid_Mort with census
Opioid_Mort_Census = pd.merge(Opioid_Mort_Fips_cleaned,Census, left_on  = ['fips','Year'],right_on= ['County Code','Year'], how = 'left',validate = '1:1')

# check # of counties in FL
if len(Opioid_Mort_Census.loc[Opioid_Mort_Census['State_x']=='FL']['County_x'].unique()) == 67:
    print('Correct, #of counties in FL is 67')
# print # of counties in other sates:

#check if all counties are assigned with pop and MME
print(Opioid_Mort_Census['MME'].isna().sum())
print(Opioid_Mort_Census['Population'].isna().sum())

# fill 0 in Nan value of deaths
Opioid_Mort_Census.loc[:,'Deaths'].fillna(0,inplace = True)
Opioid_Mort_Census_cleaned= Opioid_Mort_Census[['County_x','Deaths','MME','State_x','Year','County Code','Population']]
Opioid_Mort_Census_cleaned[['Deaths','County Code','Population']] = Opioid_Mort_Census_cleaned[['Deaths','County Code','Population']].astype('int')
Opioid_Mort_Census_cleaned.rename(columns = {'County_x':'County','State_x':'State','Year_x':'Year'},inplace = True)
Opioid_Mort_Census_cleaned['State'].value_counts()

#check dtypes
Opioid_Mort_Census_cleaned.dtypes

Opioid_Mort_Census_cleaned.to_csv('45_Opioid_Mort_Census_cleaned.csv')
