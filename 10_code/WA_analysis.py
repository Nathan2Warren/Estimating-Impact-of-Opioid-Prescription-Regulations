import pandas as pd
import numpy as np
from plotnine import *

state = 'WA'

### Functions ###
def subseter (x):
    search1 = state
    search2 = "Drug poisonings"

    state_select = x["County"].str.endswith(search1, na=False)
    x = x[state_select]
    drug_select = x["Drug/Alcohol Induced Cause"].str.startswith(search2, na=False)
    return x[drug_select]

df = pd.read_csv('C:/Users/Jiajie Zhang/PDSTeam9 Dropbox/10_intermediate_data/WA_cleaned_and_merged.csv')
##df.loc[df['Year']==2010]
### group by Year
By_Year = df.groupby('Year')['QUANTITY','Deaths'].sum()
By_Year

Mortality = pd.read_csv("C:/Users/Jiajie Zhang/PDSTeam9 Dropbox/10_intermediate_data/Mortality_Full.csv")
Mortality = subseter(Mortality)
Mortality['Deaths'] = Mortality['Deaths'].str.rstrip('.0')
Mortality['Deaths'] = Mortality['Deaths'].astype(int)
Mortality.dtypes
Mort_By_Year = Mortality.groupby('Year')['Deaths'].sum()
Mort_By_Year
