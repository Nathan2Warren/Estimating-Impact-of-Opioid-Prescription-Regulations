import pyarrow
import pandas as pd
#Import dataset
df_check = pd.read_csv("/Users/N1/690 local/arcos_all_washpost.tsv", nrows = 20, sep = "\t")

#Check column names to find column to filter by
for col in  df_check.columns:
    print(col)
    pass

#Check how BUYER_STATE values are stored
df_check['BUYER_STATE']

#Filter out for Florida by x amount of rows
iter_csv = pd.read_csv("/Users/N1/690 local/arcos_all_washpost.tsv", iterator=True, sep = "\t", chunksize = 1000000)
FL_data = pd.concat(   [chunk[chunk['BUYER_STATE']  == "FL"] for chunk in iter_csv]   )

#Make sure everything came out right
FL_data.head()

#Check # of rows
FL_data.shape

#Saving to CSV
FL_data.to_csv('/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/FL_Opioid_data.csv')

#Attempting to save to parquet but did not work (for reference in future)
#FL_data.to_parquet('/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/FL_data.parquet',  engine='pyarrow')
