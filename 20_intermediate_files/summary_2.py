import pandas as pd
GA = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-3/master/20_intermediate_files/GA_cleaned_and_merged.csv?token=AKAKVRCCA4ELK4BABSXAUUS534CIK')
GA.head()
GA.groupby(['County']).sum()
### 154 Counties in GA state
IL = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-3/master/20_intermediate_files/IL_cleaned_and_merged.csv?token=AKAKVREPYBKCIBU6Y7GXSCS534CYM')
IL.head()
IL.groupby(['County']).sum()
### 102 Counties in IL state
IN = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-3/master/20_intermediate_files/IN_cleaned_and_merged.csv?token=AKAKVRG4XBD2FYEZIPFAY62534C5Q')
IN.groupby(['County']).sum()
### 92 counties in IN state

OH = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-3/master/20_intermediate_files/OH_cleaned_and_merged.csv?token=AKAKVRGCMRSTD3IQBNY67MS534DB4')
OH.groupby(['County']).sum()
### 88 Counties in OH state

PA = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-3/master/20_intermediate_files/PA_cleaned_and_merged.csv?token=AKAKVRGEW35XDMSXI2DPPZS534DJC')
PA.groupby(['County']).sum()
### 67 counties in PA state
TX = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-3/master/20_intermediate_files/TX_cleaned_and_merged.csv?token=AKAKVRBTGCGRNIMLTLYUMFS534DZC')
TX.groupby(['County']).sum()
### 236 counties in TX state

WA = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-3/master/20_intermediate_files/WA_cleaned_and_merged.csv?token=AKAKVRGRX24Q3XKZMBV7UF2534D5C')
WA = WA.groupby(['County']).sum()
WA.shape
### 39 counties in WA state

FL = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-3/master/20_intermediate_files/FL_cleaned_and_merged.csv?token=AKAKVRBHJ4LUKHGM4ZZJM7S534EFE')
FL.groupby(['County']).sum()
### 67 counties in FL state
