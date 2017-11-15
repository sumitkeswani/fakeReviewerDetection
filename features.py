'''
This file will be used to calculate features for a reviewer
'''

import pandas as pd
from collections import defaultdict

def kde(grouped_df):
	product_ratings_list = []

	for index, row in grouped_df.iterrows():
		for index_list, val in enumerate(row['asin']):
			product_ratings_list.append([val, grouped_df.ix[index,'overall'][index_list], grouped_df.ix[index,'reviewTime'][index_list]])
	product_ratings = pd.DataFrame(product_ratings_list, columns=["product_id", "rating", "date"])
	grouped_pr = pd.DataFrame(columns=product_ratings.columns.values)
	grouped_pr["rating"] = product_ratings.groupby("product_id")["rating"].apply(list)
	grouped_pr["date"] = product_ratings.groupby("product_id")["date"].apply(list)
	grouped_pr.drop('product_id', axis=1, inplace=True)
	return grouped_pr

#creates a seperate column "rating_deviation" in df_grouped - saves the rating deviation for each reviewer
def rating_deviation(grouped_df):
    average = lambda n : sum(n) / len(n)
    average_rating_product = defaultdict(list)
    overall_df = grouped_df['overall'].to_frame()

    # finds the list of rating for each product (key) in the dictionary average_rating_product
    for index, row in grouped_df.iterrows():
        for index_list, val in enumerate(row['asin']):
            average_rating_product[val].append(grouped_df.ix[index,'overall'][index_list])

    # finds the average rating for each product (key) in the dictionary average_rating_product
    for key in average_rating_product:
        average_rating_product[key] = sum(average_rating_product[key])/len(average_rating_product[key])

    a = []

    #stores the rating deviation for each product in df_grouped
    for index, row in grouped_df.iterrows():
        for index_list, val in enumerate(row['overall']):
            a.append((val - average_rating_product[grouped_df.ix[index, 'asin'][index_list]]) / 4)
        grouped_df.ix[index, 'rating_deviation'] = average(a)
        a = []

    return grouped_df

if __name__ == '__main__':

    csv_file = "./raw_data.csv"

    # input dataframe
    music_df = pd.DataFrame.from_csv(csv_file, sep="\t")

    # Final output dataframe
    column_names = ["reviewerID", "products", "avg_helpfulness", "rating_deviation", "similarity",
                    "common_burst_time_frame", "burst_ratio"]
    df = pd.DataFrame(columns=column_names)

    # group data over reviewerIDs
    grouped_df = pd.DataFrame(columns=music_df.columns.values)
    for col in music_df.columns.values:
        if (col == "reviewerID"): continue
        grouped_df[col] = music_df.groupby("reviewerID")[col].apply(list)
    # print grouped_df

    # ans = rating_deviation(grouped_df)
    # grouped_df = ans

    # print grouped_df['rating_deviation']
    print kde(grouped_df)

