import pandas as pd
import numpy as np
import os
from plotnine import *

os.chdir('C:/Users/Jiajie Zhang/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files')
os.getcwd()
#read in files
df =  pd.read_csv('17_mortality_pop_county_level.csv')
len(df.loc[df['State']=='FL']['County'].unique())

def prepost_plot(Target_State, policy_year):
    ###read dataset
    df =  pd.read_csv('17_mortality_pop_county_level.csv')
    States = [Target_State]

    # subset dataset
    mask = df['State'].isin(States)
    Mortality_Pop = df.loc[mask]

    # calculate deaths per poppulation
    Mortality_Pop['Deaths_Per_100000'] = Mortality_Pop['Deaths']/Mortality_Pop['Population']*100000
    Mortality_Pop['Is_Target_State'] = Mortality_Pop['State'] == States[0]

    p = (ggplot() +
        #geom_line(Mortality_Pop.loc[Mortality_Pop['after_policy_year']==True], aes( x = 'Year', y ='Pred_Deaths_per_Pop'), color = "red") +
        geom_smooth(Mortality_Pop.loc[(Mortality_Pop['Year']>=policy_year) ], aes( x = 'Year', y = 'Deaths_Per_100000',color = 'Is_Target_State'), method = 'lm') +
        geom_smooth(Mortality_Pop.loc[(Mortality_Pop['Year']<=(policy_year-1))], aes( x = 'Year', y ='Deaths_Per_100000',color = 'Is_Target_State'), method = 'lm') +
        geom_vline(xintercept = policy_year,colour="#BB0000") +
        ggtitle('{} Overdose Mortality Prepost Analysis'.format(States[0]))
        #ylim(0,1)
    )

    (ggsave(filename = '../30_results/{}_Prepost_Analysis'.format(States[0]),plot = p,width =12, height = 8))

prepost_plot('FL',2010)
prepost_plot('TX',2007)
prepost_plot('WA',2012)
