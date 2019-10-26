"""
import pandas as pd

#Read file
FL_Opiate = pd.read_csv('/Users/N1/690 local/FL_data.csv', low_memory = False)
FL_Opiate.head()

#This value was not letting me save as parquet #potential data cleaning we need to do, dropped the column for now
#Same for ORDER_FORM_NO
FL_Opiate.loc[FL_Opiate['NDC_NO'] == '000913816**']
FL_Opiate = FL_Opiate.drop("NDC_NO", axis =1)
FL_Opiate = FL_Opiate.drop("ORDER_FORM_NO", axis =1)

#Check that these columns were dropped
for col in  FL_Opiate.columns:
    print(col)
    pass

#Save to parquet
FL_Opiate.to_parquet('/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/FLopiate.parquet', engine = 'fastparquet')
