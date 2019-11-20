import pandas as pd
import os
from plotnine import *


os.chdir("/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files/")

# Load Data and create list of states
Census = pd.read_csv("/Users/N1/Desktop/Census_Full.csv", header=0)
State_list = Census['Geography'].unique()
State_list
Census = Census.melt(id_vars=["Geography"],
                     var_name="Year",
                     value_name="Population")
# Make a dictionary of State names to abbreviations
Replace_list = State_list
Replace_fixed = ['USA', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
                 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
Replace_dict = dict(zip(Replace_list, Replace_fixed))
Replace_dict

# Replace State names with 2 letter abbreviations
Census['Geography'].replace(Replace_dict, inplace=True)
Census.rename(columns={'Geography': 'State'}, inplace=True)


Grouped = pd.read_csv(
    "/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files/15_Grouped_Population_Death_Data.csv")

# Match types for merging
Census['Year'] = Census['Year'].astype(int)
Grouped['Year'] = Grouped['Year'].astype(float).astype(int)

# Merge
Merged = pd.merge(Grouped, Census, how='left', on=['Year', 'State'], validate='1:1')
Merged = Merged.drop('Unnamed: 0', axis=1)
Merged.head(20)
Merged['Deaths_Normalized'] = Merged.Deaths/Merged.Population * 100000

# Save checkpoint to csv
Merged.to_csv("/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files/16_Merged_Population_Death_Data.csv")

# Plot out in one graph // not used
# (ggplot(Merged, aes(x='Year', y='Deaths_Normalized', group='State', color='State')) +
# geom_point(alpha=.9)
# )

# Plot out using facet_wrap & save
# Size looks big in python but is smaller when the plot is saved
p = (ggplot(Merged, aes(x='Year', y='Deaths_Normalized', color='State')) +
     geom_line(size=1) +
     facet_wrap('State') +
     ggtitle('Normalized Deaths 2003 - 2016') +
     theme(axis_text_x=element_text(angle=90, size=7)) +
     ylab("Deaths per Capita (100k)") +
     scale_x_continuous(breaks=[2003, 2007, 2011, 2015]) +
     scale_color_discrete(guide=False) +
     theme(plot_title=element_text(size=20))
     #theme(panel_background=element_rect(fill="gray", alpha = .2))
     )
(ggsave(p, width=10, height=10))
