import pandas as pd
import numpy as np
import os
os.chdir('C:/Users/Jiajie Zhang/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files')
os.getcwd()
Census =  pd.read_csv('21_Census_Full_County_Level.csv')
Mortality = pd.read_csv('15_Drug_Mortality_Full.csv')
Mortality_Pop = pd.merge(Census,Mortality, on=['County Code','Year'], how = 'left')
len(Mortality_Pop.loc[Mortality_Pop['State_x']=='FL']['County Code'].unique())

Mortality_Pop = Mortality_Pop.drop(columns = ['Unnamed: 0_x','Unnamed: 0_y','State_y','County_y'])
#(Mortality['Deaths'].isnull()==True).index()
Mortality_Pop.rename(columns  = {'State_x':'State', 'County_x':'County'},inplace=True)
## recasting
Mortality_Pop['Deaths'] = Mortality_Pop['Deaths'].fillna(0).astype('int')
Mortality_Pop['Population'] = Mortality_Pop['Population'].astype('int')
Mortality_Pop.loc[Mortality_Pop['Population'].isna()]
Mortality_Pop.to_csv('17_mortality_pop_county_level.csv')
