#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
import pandas as pd 
import zipfile
import numpy as np
from plotnine import *
import matplotlib as mpl


# In[36]:


appended_data = pd.DataFrame()
for filename in glob.glob('../PDSTeam9 Dropbox/00_sourcedata/US_VitalStatistics\*.txt'):
    #print(filename)
    df_tmp = pd.read_csv(filename,sep = '\t')
    appended_data = appended_data.append(df_tmp)


# In[37]:


appended_data[['County','State']] = appended_data.County.str.split(', ',expand = True)
appended_data


# In[38]:


appended_data_dropna = appended_data.dropna(thresh = 5)
appended_data_dropna


# In[39]:


def subseter (x):
    search2 = "Drug poisonings"
    Y = x["Drug/Alcohol Induced Cause"].str.startswith(search2, na=False)
    return x[Y]


# In[40]:


Drug_mortality_allstate = subseter(appended_data_dropna)
Drug_mortality_allstate['Drug/Alcohol Induced Cause Code'].value_counts()


# In[52]:


Drug_mortality_allstate['Deaths'] = Drug_mortality_allstate['Deaths'].replace('Missing',np.nan)


# In[56]:


#Drug_mortality_allstate.loc[Drug_mortality_allstate['Deaths']=='Missing'] = np.nan


# In[57]:


#Drug_mortality_allstate.loc[['Deaths']]


# In[59]:


Drug_mortality_allstate['Deaths'] = Drug_mortality_allstate['Deaths'].astype('float64',copy = False)


# In[60]:


for i in Drug_mortality_allstate['Deaths'].value_counts().index: print(type(i),i)


# In[61]:


sort = Drug_mortality_allstate.sort_values(by='Deaths')


# In[62]:


sort


# In[63]:


#Group data by Year and State
Grouped = Drug_mortality_allstate.groupby(['State','Year'],as_index=False)['Deaths'].sum()


# In[77]:


Grouped


# In[74]:


(ggplot(Grouped, aes(x ='Year', y='Deaths',group = 'State',color='State'))+
geom_point(alpha=0.2)+geom_line() 
) 


# In[87]:


p=(ggplot(Grouped, aes(x ='Year', y='Deaths',group = 'State',color='State'))+
geom_point(alpha=0.2)+geom_line() +
facet_wrap('State')
)
(ggsave(p,width =10, height = 10))


# In[ ]:




