import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-3/master/20_intermediate_files/45_Opioid_Mort_Census_cleaned.csv?token=AKAKVRGPHBGBUYL3FAYTSC254SBTG')
df.head()

MME2006 = print(df[df.Year == 2006].MME.sum())
MME2007 = print(df[df.Year == 2007].MME.sum())
MME2008 = print(df[df.Year == 2008].MME.sum())
MME2009 = print(df[df.Year == 2009].MME.sum())
MME2010 = print(df[df.Year == 2010].MME.sum())
MME2011 = print(df[df.Year == 2011].MME.sum())
MME2012 = print(df[df.Year == 2012].MME.sum())

Death2006 = print(df[df.Year == 2006].Deaths.sum())
Death2007 = print(df[df.Year == 2007].Deaths.sum())
Death2008 = print(df[df.Year == 2008].Deaths.sum())
Death2009 = print(df[df.Year == 2009].Deaths.sum())
Death2010 = print(df[df.Year == 2010].Deaths.sum())
Death2011 = print(df[df.Year == 2011].Deaths.sum())
Death2012 = print(df[df.Year == 2012].Deaths.sum())

MMEper2006 = print(df[df.Year == 2006].MME.sum() / df[df.Year == 2006].Population.sum())
MMEper2007 = print(df[df.Year == 2007].MME.sum() / df[df.Year == 2007].Population.sum())
MMEper2008 = print(df[df.Year == 2008].MME.sum() / df[df.Year == 2008].Population.sum())
MMEper2009 = print(df[df.Year == 2009].MME.sum() / df[df.Year == 2009].Population.sum())
MMEper2010 = print(df[df.Year == 2010].MME.sum() / df[df.Year == 2010].Population.sum())
MMEper2011 = print(df[df.Year == 2011].MME.sum() / df[df.Year == 2011].Population.sum())
MMEper2012 = print(df[df.Year == 2006].MME.sum() / df[df.Year == 2012].Population.sum())

Deathper2006 = print(df[df.Year == 2006].Deaths.sum() / df[df.Year == 2006].Population.sum())
Deathper2007 = print(df[df.Year == 2007].Deaths.sum() / df[df.Year == 2007].Population.sum())
Deathper2008 = print(df[df.Year == 2008].Deaths.sum() / df[df.Year == 2008].Population.sum())
Deathper2009 = print(df[df.Year == 2009].Deaths.sum() / df[df.Year == 2009].Population.sum())
Deathper2010 = print(df[df.Year == 2010].Deaths.sum() / df[df.Year == 2010].Population.sum())
Deathper2011 = print(df[df.Year == 2011].Deaths.sum() / df[df.Year == 2011].Population.sum())
Deathper2012 = print(df[df.Year == 2012].Deaths.sum() / df[df.Year == 2012].Population.sum())

from pandas import DataFrame
data = {'Year':['2006','2007','2008','2009','2010','2011','2012'], 'MME/Capita':['0.25634691103596535','0.29729474376455006','0.3380123523745701','0.3875592528147102','0.4492204699226896','0.4148365814898084','0.24196307940097167']}
MME = DataFrame(data,columns=['Year','MME/Capita'])

from pandas import DataFrame
data = {'Year':['2006','2007','2008','2009','2010','2011','2012'], 'Deaths/Capita':['8.70235304058954e-05','8.568355897942634e-05','8.958405636666133e-05','9.343491539225856e-05','9.569470374046673e-05','0.00010375433824375567','9.902407573742254e-05']}
Deaths = DataFrame(data,columns=['Year','Deaths/Capita'])

from pandas import DataFrame
data = {'Year':['2006','2007','2008','2009','2010','2011','2012'], 'MME':['25610085.388993837',
'29991935.392387405',
'34429817.54246391',
'39865525.25000516',
'46717759.10185604',
'43525033.29054618',
'37882725.67251197']}
MME1 = DataFrame(data,columns=['Year','MME'])

from pandas import DataFrame
data = {'Year':['2006','2007','2008','2009','2010','2011','2012'], 'Deaths':['8694',
'8644',
'9125',
'9611',
'9952',
'10886',
'10481']}
Deaths1 = DataFrame(data,columns=['Year','Deaths'])

MME['MME Per Capita'] = MME['MME/Capita'].astype('float')
MME['year'] = MME['Year'].astype('float')

Deaths['Deaths Per Capita'] = Deaths['Deaths/Capita'].astype('float')
Deaths['year'] = Deaths['Year'].astype('float')

MME1['MME'] = MME1['MME'].astype('float')
MME1['year'] = MME1['Year'].astype('float')

Deaths1['Deaths'] = Deaths1['Deaths'].astype('float')
Deaths1['year'] = Deaths1['Year'].astype('float')

from plotnine import *
p1 = (ggplot(MME, aes(x='year', y='MME Per Capita')) +
        geom_line() +
        ggtitle('MME Per Capita by Year of All Counties')
)
(ggsave(p1, filename="MME Per Capita", width=10, height=10,
        path="/Users/chenyu/Duke/IDS 690/jupyter_lab"))

p2 = (ggplot(Deaths, aes(x='year', y='Deaths Per Capita')) +
        geom_line() +
        ggtitle('Deaths Per Capita by Year of All Counties')
)
(ggsave(p2, filename="Deaths Per Capita", width=10, height=10,
        path="/Users/chenyu/Duke/IDS 690/jupyter_lab"))
p3 = (ggplot(MME1, aes(x='year', y='MME')) +
        geom_line() +
        ggtitle('MME by Year of All Counties')
)
(ggsave(p3, filename="MME", width=10, height=10,
        path="/Users/chenyu/Duke/IDS 690/jupyter_lab"))
p4 = (ggplot(Deaths1, aes(x='year', y='Deaths')) +
        geom_line() +
        ggtitle('Deaths by Year of All Counties')
)
(ggsave(p4, filename="Deaths", width=10, height=10,
        path="/Users/chenyu/Duke/IDS 690/jupyter_lab"))
        
