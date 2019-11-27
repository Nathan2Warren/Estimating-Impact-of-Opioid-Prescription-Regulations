# Counties with zero deaths
import pandas as pd

# Load and check years
df = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-3/master/20_intermediate_files/17_mortality_pop_county_level.csv?token=AKAKVRFK2VSZEXYHCHZEHY254RN4S')
df.head(40)
df.tail(40)

# List of States
states = ['FL', 'TX', 'WA', 'PA', 'OH', 'IN', 'IL', 'GA']

# Get Percentage of zero values
for i in states:
    print(df[(df.State == i) & (df.Deaths == 0)].count()) / df[df.State == i]['Deaths'].count())

# Get count of all counties to ensure our data has the full number of counties
for i in states:
    print(df[df['State'] == i].count())

# Get count of zero death counties
for i in states:
    print(df[(df.State == i) & (df.Deaths == 0)].count())
