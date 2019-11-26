import pandas as pd
import numpy as np
import glob
import os
from plotnine import *
#define states, the first is study state, the latters are comparison states
States = ['FL','GA','IL','IN','OH','PA']
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
Opioid_Mort_Census['MME_Per_Capita'] = Opioid_Mort_Census['MME']/Opioid_Mort_Census['Population']*1000
Opioid_Mort_Census['Deaths_Per_100000'] = Opioid_Mort_Census['Deaths']/Opioid_Mort_Census['Population']*100000
Opioid_Mort_Census.to_csv('FL_Did_Opioid_Mort_Census.csv')
Opioid_Mort_Census['Counties in State with Policy Change'] = Opioid_Mort_Census['State'] == States[0]

Opioid_Mort_Census['Year'].isnull().sum()

# plot out correlations btw mort & drug in FL
FL = Opioid_Mort_Census.loc[Opioid_Mort_Census['State']=='FL']
FL['log_MME'] = np.log(FL['MME_Per_Capita'])
FL_wo_0s = Opioid_Mort_Census.loc[(Opioid_Mort_Census['State']=='FL') & (Opioid_Mort_Census['Deaths_Per_100000']!=0)]
FL_wo_0s['log_MME'] = np.log(FL_wo_0s['MME_Per_Capita'])
corr = round(FL[['log_MME','Deaths_Per_100000']].corr('pearson').values[0,1],2)
corr_wo_0s = round(FL_wo_0s[['log_MME','Deaths_Per_100000']].corr('pearson').values[0,1],2)

corrplot = (ggplot() +
geom_smooth(FL, aes( x = 'log_MME', y = 'Deaths_Per_100000'), method = 'lm',se=False,color = 'red') +
geom_point(FL,aes(x = 'log_MME', y = 'Deaths_Per_100000'),alpha = 0.5)+
ylab('Deaths Per 100k') +
xlab("log_MME Per Capita")  +
ylim(0,40) +
ggtitle('Florida log_MME-Mortality Correlation : {}'.format(corr))
)
(ggsave(filename = '../30_results/02_FL_log_Drug_Mortality_Correlation',plot = corrplot,width =12, height = 8))

corrplot2 = (ggplot() +
geom_smooth(FL_wo_0s, aes( x = 'log_MME', y = 'Deaths_Per_100000'), method = 'lm',se=False,color = 'red') +
geom_point(FL_wo_0s,aes(x = 'log_MME', y = 'Deaths_Per_100000'),alpha = 0.5)+
ylab('Deaths Per 100k') +
xlab("log_MME Per Capita")  +

ggtitle('Florida log_MME-Mortality Correlation : {}'.format(corr_wo_0s))
)
(ggsave(filename = '../30_results/03_FL_log_Drug_Mortality_Correlation_wo_0s',plot = corrplot2,width =12, height = 8))


#line_a['MME_Per_Capita'].isnull().sum()
p = (ggplot(Opioid_Mort_Census,aes( x = 'Year', y ='MME_Per_Capita')) +
theme(legend_position=(0.5,-0.01)) +
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']>=policy_year) & (Opioid_Mort_Census['Counties in State with Policy Change']==False)], aes( x = 'Year', y = 'MME_Per_Capita', color = 'Counties in State with Policy Change'), method = 'lm') +
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1)) & (Opioid_Mort_Census['Counties in State with Policy Change']==False)], aes( x = 'Year', y ='MME_Per_Capita',color = 'Counties in State with Policy Change'), method = 'lm') +
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']>=policy_year) & (Opioid_Mort_Census['Counties in State with Policy Change']==True)], aes( x = 'Year', y = 'MME_Per_Capita',color = 'Counties in State with Policy Change'), method = 'lm') +
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1)) & (Opioid_Mort_Census['Counties in State with Policy Change']==True)], aes( x = 'Year', y ='MME_Per_Capita',color = 'Counties in State with Policy Change'), method = 'lm') +
ylab("MME Per Capita")  +
#scale_fill_discrete(name = "Counties in State with Policy Change") +
geom_vline(xintercept = policy_year,colour="#BB0000") +
ggtitle('Florida MME Dosage Diff-in-Diff Analysis')
#ylim(0,1)
)
(ggsave(filename = '../30_results/FL_Drug_DiD_Analysis',plot = p,width =12, height = 8))


## add propotional change later
