from sklearn import linear_model
import pandas as pd
import numpy as np
import glob
from plotnine import *
import os

os.chdir("/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/")


# combine data in all files
appended_data = pd.DataFrame()
for filename in glob.glob('US_VitalStatistics/*.txt'):
    df_tmp = pd.read_csv(filename, sep='\t')
    appended_data = appended_data.append(df_tmp)

appended_data.head()

# Save all mortality dataset to one file
# FL_data.to_csv('US_Mortality_2003_2015.csv')
search = "TX"
search2 = "Drug poisonings"
x = appended_data['County'].str.endswith(search, na=False)
State_data = appended_data[x]
Y = State_data["Drug/Alcohol Induced Cause"].str.startswith(search2, na=False)
State_data = State_data[Y]

# change datatypes
State_data['Deaths'] = pd.to_numeric(State_data.Deaths)
State_data['Year'] = State_data['Year'].astype('int')

# expand county state to two columns
State_data[['County', 'State']] = State_data['County'].str.split(', ', expand=True)

# FL data exploration
State_deaths = State_data.groupby(['Year'], as_index=False)['Deaths'].sum()

State_pop = pd.read_csv('Individual States/TX_Census_Data2.csv')
State_pop_year = State_pop.groupby(['Year'], as_index=False)['Population'].sum()

# missing pop data b4 2010, use linear regression and append results to state_year level pop dataset
lr = linear_model.LinearRegression()
lr.fit(X=State_pop_year['Year'].values.reshape(-1, 1),
       y=State_pop_year['Population'].values.reshape(-1, 1))
X_pred = np.arange(2003, 2010).reshape(-1, 1)
y_pred = lr.predict(X_pred)
tmp = np.vstack([X_pred.flatten(), y_pred.flatten()]).T
tmp_df = pd.DataFrame(tmp,  columns=['Year', 'Population'])
State_pop_year2 = State_pop_year.copy()
State_pop_year2 = State_pop_year2.append(tmp_df).sort_values(by='Year').astype('int64')

# merge stata-year level pop and mortality dataset
merged_death_pop = pd.merge(State_deaths, State_pop_year2, on=['Year'], how='left')

# Calc relative Mortiality per cap
merged_death_pop['Deaths_per_Pop'] = merged_death_pop['Deaths'] / \
    merged_death_pop['Population'] * 100000

# fit LinearRegression for mortlaity prediction after policy change
lr2 = linear_model.LinearRegression()
lr2.fit(X=merged_death_pop['Year'][:4].values.reshape(-1, 1),
        y=merged_death_pop['Deaths_per_Pop'][:4].values.reshape(-1, 1))
merged_death_pop['Pred_Deaths_per_Pop'] = lr2.predict(
    merged_death_pop['Year'].values.reshape(-1, 1)).flatten().T

# Texas plot
TX_PLOT = (ggplot(Texas, aes(x='Year', y='Deaths_per_Pop')) +
           geom_smooth(Texas.loc[Texas['Year'] >= 2007], aes(x='Year', y='Pred_Deaths_per_Pop'), method='lm', color="red") +
           geom_smooth(Texas.loc[Texas['Year'] >= 2007], aes(x='Year', y='Deaths_per_Pop'), method='lm', color="black") +
           geom_smooth(Texas.loc[Texas['Year'] <= 2006], aes(x='Year', y='Deaths_per_Pop'), method='lm', color="black") +
           geom_vline(xintercept=2007, colour="#BB0000") +
           ggtitle('Texas Mortiality: Pre-Post Analysis') +
           xlim(2002, 2015) +
           ylab('Deaths per Capita (100k)')
           )


# Write file to csv
merged_death_pop.to_csv(
    "/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files/50_Texas_Prepost.csv")
