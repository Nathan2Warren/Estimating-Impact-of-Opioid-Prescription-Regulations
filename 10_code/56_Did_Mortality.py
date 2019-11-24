import pandas as pd
import numpy as np
import glob
import os
from plotnine import *
os.chdir('C:/Users/Jiajie Zhang/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files')
os.getcwd()
df =  pd.read_csv('17_mortality_pop_county_level.csv')
len(df.loc[df['State']=='FL']['County'].unique())
## inputs
#Target_State  = ['FL']
#policy_year = 2010

def did_plot(Target_State, policy_year):
    ###read dataset
    df =  pd.read_csv('17_mortality_pop_county_level.csv')
    States = [Target_State,'GA','IL','IN','OH','PA']

    # subset dataset
    mask = df['State'].isin(States)
    Mortality_Pop = df.loc[mask]

    # calculate deaths per poppulation
    Mortality_Pop['Deaths_Per_100000'] = Mortality_Pop['Deaths']/Mortality_Pop['Population']*100000
    Mortality_Pop['Is_Target_State'] = Mortality_Pop['State'] == States[0]

    p = (ggplot() +
        #geom_line(Mortality_Pop.loc[Mortality_Pop['after_policy_year']==True], aes( x = 'Year', y ='Pred_Deaths_per_Pop'), color = "red") +
        geom_smooth(Mortality_Pop.loc[(Mortality_Pop['Year']>=policy_year) & (Mortality_Pop['Is_Target_State']==False)], aes( x = 'Year', y = 'Deaths_Per_100000', color = 'Is_Target_State'),method = 'lm') +
        geom_smooth(Mortality_Pop.loc[(Mortality_Pop['Year']<=(policy_year-1)) & (Mortality_Pop['Is_Target_State']==False)], aes( x = 'Year', y ='Deaths_Per_100000',color = 'Is_Target_State'), method = 'lm') +
        geom_smooth(Mortality_Pop.loc[(Mortality_Pop['Year']>=policy_year) & (Mortality_Pop['Is_Target_State']==True)], aes( x = 'Year', y = 'Deaths_Per_100000',color = 'Is_Target_State'), method = 'lm') +
        geom_smooth(Mortality_Pop.loc[(Mortality_Pop['Year']<=(policy_year-1)) & (Mortality_Pop['Is_Target_State']==True)], aes( x = 'Year', y ='Deaths_Per_100000',color = 'Is_Target_State'), method = 'lm') +
        ##geom_point(Mortality_Pop.loc[(Mortality_Pop['Year']>=policy_year) & (Mortality_Pop['Is_Target_State']==False)], aes( x = 'Year', y = 'Deaths_Per_100000'), color = "black") +
        ##geom_point(Mortality_Pop.loc[(Mortality_Pop['Year']<=(policy_year-1)) & (Mortality_Pop['Is_Target_State']==False)], aes( x = 'Year', y ='Deaths_Per_100000'),color = "black") +
        #geom_point(Mortality_Pop.loc[(Mortality_Pop['Year']>=policy_year) & (Mortality_Pop['Is_Target_State']==True)], aes( x = 'Year', y = 'Deaths_Per_100000'), color = "blue") +
        #geom_point(Mortality_Pop.loc[(Mortality_Pop['Year']<=(policy_year-1)) & (Mortality_Pop['Is_Target_State']==True)], aes( x = 'Year', y ='Deaths_Per_100000'),color = "blue") +
        geom_vline(xintercept = policy_year,colour="#BB0000") +
        ggtitle('{} Overdose Mortality Diff-in-Diff Analysis'.format(States[0]))
        #ylim(0,1)
    )

    (ggsave(filename = '../30_results/{}_DiD_Analysis'.format(States[0]),plot = p,width =12, height = 8))

did_plot('FL',2010)
did_plot('TX',2007)
did_plot('WA',2012)
