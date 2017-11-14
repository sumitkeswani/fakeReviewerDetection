'''
This file will be used to calculate features for a reviewer
'''

import pandas as pd

csv_file = "./raw_data.csv"

# input dataframe
music_df = pd.DataFrame.from_csv(csv_file, sep="\t")

# Final output dataframe
column_names = ["reviewerID", "products", "avg_helpfulness", "rating_deviation", "similarity", "common_burst_time_frame", "burst_ratio"]
df = pd.DataFrame(columns = column_names)

# group data over reviewerIDs
grouped_df = pd.DataFrame(columns=music_df.columns.values)
for col in music_df.columns.values:
    if(col == "reviewerID"): continue
    grouped_df[col] = music_df.groupby("reviewerID")[col].apply(list)

    
print grouped_df

