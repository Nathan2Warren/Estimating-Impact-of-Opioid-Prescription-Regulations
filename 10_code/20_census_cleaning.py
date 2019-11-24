import pandas as pd
import numpy as np
from sklearn import linear_model
import os
os.chdir('C:/Users/Jiajie Zhang/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files')
os.getcwd()
df = pd.read_csv('./Census_raw.csv',encoding = 'latin-1')
State_code = pd.read_csv('00_State_code.csv',index_col = 'State')
State_code_dict = State_code.to_dict()
State_code_dict = State_code_dict['Code']

Census  =df.drop(columns = ['GEO.id','rescen42010','resbase42010'])
#reset column names
Census.columns = ['County Code','Geography','2010','2011','2012','2013','2014','2015','2016','2017','2018']
Census[['County', 'State']] = Census['Geography'].str.split(', ', expand=True)
Census = Census.drop(columns = 'Geography')
Census['County'] = Census['County'].str.replace(' County','')
Census['County'] = Census['County'].str.upper()
Census['State'].replace(State_code_dict,inplace = True)
Census.loc[Census['State'] == 'FL']

Census.drop(index = 0,inplace = True)
Census=Census.reset_index(drop = True)
# extropolate Population to 2003-2010
Year = np.arange(2010,2019).reshape(-1,1)
Pred_Year = np.arange(2003,2010).reshape(-1,1)
#Pred = np.array([]).reshape(Pred_Year.shape)
Pred = np.array([]).reshape(-1,7)
for i in range(Census.shape[0]):
    lr = linear_model.LinearRegression()
    lr.fit(X= Year,y=Census.iloc[i,1:-2])
    y_pred = lr.predict(Pred_Year)
    Pred = np.vstack((Pred,y_pred))
#convert prediction result to df
columns = ['2003','2004','2005','2006','2007','2008','2009']
Pred_df =pd.DataFrame(Pred,columns = columns).astype('int')

#merge and reorder columns
Merged_Census = Census.merge(Pred_df,left_index =True,right_index = True)
Merged_Census = Merged_Census[['State','County','County Code','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]

#Merged_Census = Merged_Census.set_index('Geography')
Melted_Census = Merged_Census.melt(id_vars = ['State','County','County Code'],var_name = 'Year',value_name = 'Population')
len(Melted_Census.loc[Melted_Census['State']=='FL'])

#save
Melted_Census.to_csv('21_Census_Full_County_Level.csv')
