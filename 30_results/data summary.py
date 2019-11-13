import pandas as pd
FL = pd.read_parquet('FLopiate.parquet',engine='pyarrow')
pd.set_option('display.max_columns', None)

FL['MME'] = FL.DOSAGE_UNIT * FL.MME_Conversion_Factor
FL.drop(['DOSAGE_UNIT', 'MME_Conversion_Factor'], axis=1, inplace=True)
FL.describe()



TX = pd.read_csv('TX_Opioid_data.csv')
TX.describe()

WA = pd.read_csv('WA_Opioid_data.csv')
WA.describe()

FLmortality = pd.read_csv('Mortality_Full.csv')
FLmortality.head()
