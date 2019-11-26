import pandas as pd
import numpy as np
import glob
import os
from plotnine import *
from sklearn import linear_model
#define states, the first is study state, the latters are comparison states
States = ['FL']
policy_year = 2010
os.chdir('C:/Users/Jiajie Zhang/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files')
os.getcwd()


Opioid_Mort_Census = pd.read_csv('45_Opioid_Mort_Census_cleaned.csv')
Opioid_Mort_Census.loc[Opioid_Mort_Census['State']=='FL'].sort_values('MME',ascending=False)


# subset needed states
mask = Opioid_Mort_Census['State'].isin(States)
Opioid_Mort_Census = Opioid_Mort_Census.loc[mask]
#validate
Opioid_Mort_Census['State'].value_counts()
Opioid_Mort_Census = Opioid_Mort_Census.drop(columns = 'Unnamed: 0')

# Calculate Deaths per 100,000 people & MME per capita
Opioid_Mort_Census['MME_Per_Capita'] = Opioid_Mort_Census['MME']/Opioid_Mort_Census['Population']*1000
Opioid_Mort_Census['Deaths_Per_100000'] = Opioid_Mort_Census['Deaths']/Opioid_Mort_Census['Population']*100000
#Opioid_Mort_Census.to_csv('FL_Did_Opioid_Mort_Census.csv')
Opioid_Mort_Census['Is_Target_State'] = Opioid_Mort_Census['State'] == States[0]
Opioid_Mort_Census['Extrapolate Prediction'] = Opioid_Mort_Census['Year'] >=policy_year
# subtract comparison States and average over population
lr = linear_model.LinearRegression()

X = Opioid_Mort_Census.loc[Opioid_Mort_Census['Extrapolate Prediction'] !=True]['Year'].values.reshape(-1,1)
y = Opioid_Mort_Census.loc[Opioid_Mort_Census['Extrapolate Prediction'] !=True]['MME_Per_Capita'].values.reshape(-1,1)

lr.fit(X,y)
Opioid_Mort_Census['Pred_MME_Per_Capita'] = lr.predict(Opioid_Mort_Census['Year'].values.reshape(-1,1)).flatten().T

p = (ggplot(Opioid_Mort_Census,aes( x = 'Year', y ='MME_Per_Capita')) +
geom_line(Opioid_Mort_Census.loc[Opioid_Mort_Census['Year']>=policy_year], aes( x = 'Year', y ='Pred_MME_Per_Capita',colour = 'Extrapolate Prediction'), linetype = "dashed")+
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']>=policy_year)], aes( x = 'Year', y = 'MME_Per_Capita'),color = "#5bd4db",size =1, method = 'lm') +
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1))], aes( x = 'Year', y ='MME_Per_Capita',colour = 'Extrapolate Prediction'), method = 'lm') +
theme(legend_position=(0.5,-0.01)) +
#labs(fill = "Counties in State with Policy Change") +
ylab("MME Per Capita")  +
geom_vline(xintercept = policy_year,colour="#BB0000") +
ggtitle('Florida MME Dosage Pre-Post Analysis')
#ylim(0,1)
)
(ggsave(filename = '../30_results/FL_Drug_Prepost_Analysis',plot = p,width =12, height = 8))
