import pandas as pd
import numpy as np
import glob
import os
from plotnine import *
#define states, the first is study state, the latters are comparison states
States = ['FL']
policy_year = 2010
os.chdir('C:/Users/Jiajie Zhang/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files')
os.getcwd()


Opioid_Mort_Census = pd.read_csv('45_Opioid_Mort_Census_cleaned.csv')

# subset needed states
mask = Opioid_Mort_Census['State'].isin(States)
Opioid_Mort_Census = Opioid_Mort_Census.loc[mask]
#validate
Opioid_Mort_Census['State'].value_counts()
Opioid_Mort_Census = Opioid_Mort_Census.drop(columns = 'Unnamed: 0')

# Calculate Deaths per 100,000 people & MME per capita
Opioid_Mort_Census['MME_Per_Capita'] = Opioid_Mort_Census['MME']/Opioid_Mort_Census['Population']
Opioid_Mort_Census['Deaths_Per_100000'] = Opioid_Mort_Census['Deaths']/Opioid_Mort_Census['Population']*100000
Opioid_Mort_Census.to_csv('FL_Did_Opioid_Mort_Census.csv')
Opioid_Mort_Census['Is_Target_State'] = Opioid_Mort_Census['State'] == States[0]
# subtract comparison States and average over population

p = (ggplot(Opioid_Mort_Census,aes( x = 'Year', y ='MME_Per_Capita')) +
#geom_line(Opioid_Mort_Census.loc[Opioid_Mort_Census['after_policy_year']==True], aes( x = 'Year', y ='Pred_Deaths_per_Pop'), color = "red") +
#geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']>=policy_year) & (Opioid_Mort_Census['Is_Target_State']==False)], aes( x = 'Year', y = 'MME_Per_Capita', color = 'Is_Target_State'), method = 'lm') +
#geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1)) & (Opioid_Mort_Census['Is_Target_State']==False)], aes( x = 'Year', y ='MME_Per_Capita',color = 'Is_Target_State'), method = 'lm') +
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']>=policy_year) & (Opioid_Mort_Census['Is_Target_State']==True)], aes( x = 'Year', y = 'MME_Per_Capita',color = 'Is_Target_State'), method = 'lm') +
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1)) & (Opioid_Mort_Census['Is_Target_State']==True)], aes( x = 'Year', y ='MME_Per_Capita',color = 'Is_Target_State'), method = 'lm') +
#geom_point(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']>=policy_year) & (Opioid_Mort_Census['Is_Target_State']==False)], aes( x = 'Year', y = 'MME_Per_Capita'), color = "black") +
#geom_point(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1)) & (Opioid_Mort_Census['Is_Target_State']==False)], aes( x = 'Year', y ='MME_Per_Capita'),color = "black") +
#geom_point(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']>=policy_year) & (Opioid_Mort_Census['Is_Target_State']==True)], aes( x = 'Year', y = 'MME_Per_Capita'), color = "blue") +
#geom_point(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1)) & (Opioid_Mort_Census['Is_Target_State']==True)], aes( x = 'Year', y ='MME_Per_Capita'),color = "blue") +

geom_vline(xintercept = policy_year,colour="#BB0000") +
ggtitle('FL Drug Shipment Pre-Post Analysis')
#ylim(0,1)
)
(ggsave(filename = '../30_results/FL_Drug_Prepost_Analysis',plot = p,width =12, height = 8))
