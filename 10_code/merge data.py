import pandas as pd
dataset = pd.read_parquet('FLopiate.parquet',engine='pyarrow')
pd.set_option('display.max_columns', None)
dataset.head(5)


dataset['MME'] = dataset.DOSAGE_UNIT * dataset.MME_Conversion_Factor
dataset.drop(['DOSAGE_UNIT', 'MME_Conversion_Factor'], axis=1, inplace=True)
dataset.head()


dataset['TRANSACTION_DATE'] = dataset['TRANSACTION_DATE'].astype('str')
dataset['Year'] = dataset['TRANSACTION_DATE'].str.extract('([0-9]{4}$)', expand=True)
dataset.head()

# Replace columns name
dataset.rename(columns = {'BUYER_STATE': 'State'}, inplace=True)
dataset.rename(columns = {'BUYER_COUNTY': 'County'}, inplace=True)
dataset.head()

dataset_new = dataset[['State', 'Year', 'County']]

pd.set_option('display.max_rows', None)
dataset_new['County'].value_counts()
dataset_new['Year'].value_counts()


FL_mort['County'].value_counts()
FL_mort['Year'].value_counts()


FL_mort = pd.read_csv('FL_mortality_2003_2015.csv', nrows=100)
FL_mort.head()


FL_mort['County'] = FL_mort['County'].astype(str)
FL_mort['County'] = FL_mort['County'].str.upper()
FL_mort.head()

FL_mort[['County', 'County1']] = FL_mort['County'].str.split(' COUNTY', expand=True)
FL_mort.head()

##
FL_mort['State'] = FL_mort['State'].astype(str)
FL_mort['Year'] = FL_mort['Year'].astype(str)

dataset_new['State'] = dataset_new['State'].astype(str)
dataset_new['County'] = dataset_new['County'].astype(str)
dataset_new['Year'] = dataset_new['Year'].astype(str)

FL_mort.head(5)

merge = pd.merge(dataset_new, FL_mort, how='left', on='County', indicator = True)
merge.head(5)

merge['_merge'].unique
