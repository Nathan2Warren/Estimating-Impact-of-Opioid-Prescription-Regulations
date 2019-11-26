import pandas as pd
import numpy as np
import os
from plotnine import *
import plotnine as plnine
from sklearn import linear_model
os.chdir('C:/Users/Jiajie Zhang/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files')
os.getcwd()
#read in files

df =  pd.read_csv('17_mortality_pop_county_level.csv')
States = ['FL']

# subset dataset
mask = df['State'].isin(States)
Mortality_Pop = df.loc[mask]
policy_year = 2010
full_name = 'FL'
# calculate deaths per poppulation
Mortality_Pop['Deaths_Per_100000'] = Mortality_Pop['Deaths']/Mortality_Pop['Population']*100000
Mortality_Pop['Is_Target_State'] = Mortality_Pop['State'] == States[0]

def prepost_plot(Target_State, full_name, policy_year):
    ###read dataset
    df =  pd.read_csv('17_mortality_pop_county_level.csv')
    States = [Target_State]

    # subset dataset
    mask = df['State'].isin(States)
    Mortality_Pop = df.loc[mask]

    # calculate deaths per poppulation
    Mortality_Pop['Deaths_Per_100000'] = Mortality_Pop['Deaths']/Mortality_Pop['Population']*100000
    Mortality_Pop['Is_Target_State'] = Mortality_Pop['State'] == States[0]
    Mortality_Pop['Extrapolate Prediction'] = Mortality_Pop['Year'] >=policy_year
    #add prediction column on years after policy change
    lr = linear_model.LinearRegression()

    X = Mortality_Pop.loc[Mortality_Pop['Extrapolate Prediction'] !=True]['Year'].values.reshape(-1,1)
    y = Mortality_Pop.loc[Mortality_Pop['Extrapolate Prediction'] !=True]['Deaths_Per_100000'].values.reshape(-1,1)

    lr.fit(X,y)
    Mortality_Pop['Pred_Deaths_per_100000'] = lr.predict(Mortality_Pop['Year'].values.reshape(-1,1)).flatten().T

    p = (ggplot() +theme(legend_position=(0.5,-0.01)) +
        #geom_line(Mortality_Pop.loc[Mortality_Pop['after_policy_year']==True], aes( x = 'Year', y ='Pred_Deaths_per_Pop'), color = "red") +
        geom_line(Mortality_Pop.loc[Mortality_Pop['Year']>=policy_year], aes( x = 'Year', y ='Pred_Deaths_per_100000',colour = 'Extrapolate Prediction'), linetype = "dashed")+
        #geom_line(Mortality_Pop.loc[(Mortality_Pop['Year']<=(policy_year-1))], aes( x = 'Year', y ='Deaths_Per_100000',colour = 'Before_PC')) +
        geom_smooth(Mortality_Pop.loc[(Mortality_Pop['Year']>=policy_year) ], aes( x = 'Year', y = 'Deaths_Per_100000'),colour = '#5bd4db',size = 1,method = 'lm') +
        geom_smooth(Mortality_Pop.loc[(Mortality_Pop['Year']<=(policy_year-1))], aes( x = 'Year', y ='Pred_Deaths_per_100000',colour = 'Extrapolate Prediction'), method = 'lm') +
        #geom_point(Mortality_Pop.loc[(Mortality_Pop['Year']<=(policy_year-1))], aes( x = 'Year', y ='Deaths_Per_100000'),color = 'red') +
        geom_vline(xintercept = policy_year,colour="#BB0000") +
        ylab("Deaths Per 100k")  +
        ggtitle('{} Drug Overdose Mortality Prepost Analysis'.format(full_name)) +
        scale_x_continuous(breaks = [2003,2006,2009,2012,2015])
    )
    (ggsave(filename = '../30_results/{}_Prepost_Analysis'.format(States[0]),plot = p,width =12, height = 8))
    return p
p1 = prepost_plot('FL','Florida',2010)
p2 = prepost_plot('TX','Texas',2007)
p3 = prepost_plot('WA','Washington',2012)
