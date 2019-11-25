

### county with zero death
import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-3/master/20_intermediate_files/17_mortality_pop_county_level.csv?token=AKAKVRFK2VSZEXYHCHZEHY254RN4S')
df.head()
print(df[(df.State == 'FL') & (df.Deaths == 0)].count() / df[df.State == 'FL']['Deaths'].count())

print(df[(df.State == 'TX') & (df.Deaths == 0)].count() / df[df.State == 'TX']['Deaths'].count())

print(df[(df.State == 'WA') & (df.Deaths == 0)].count() / df[df.State == 'WA']['Deaths'].count())

print(df[(df.State == 'PA') & (df.Deaths == 0)].count() / df[df.State == 'PA']['Deaths'].count())

print(df[(df.State == 'OH') & (df.Deaths == 0)].count() / df[df.State == 'OH']['Deaths'].count())

print(df[(df.State == 'IN') & (df.Deaths == 0)].count() / df[df.State == 'IN']['Deaths'].count())

print(df[(df.State == 'IL') & (df.Deaths == 0)].count() / df[df.State == 'IL']['Deaths'].count())

print(df[(df.State == 'GA') & (df.Deaths == 0)].count() / df[df.State == 'GA']['Deaths'].count())
