'''
This file will be used to calculate features for a reviewer
'''

import pandas as pd
from collections import defaultdict
from sklearn.neighbors.kde import KernelDensity
import numpy as np
from datetime import datetime

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


    #Now grouped_pr contains product_id, [list of ratings], [list of dates]

    kde_list = []
    p_id = []

    for index, row in grouped_pr.iterrows():
        p_id.append(index)
        for i in range(len(grouped_pr.ix[index,'date'])):
            grouped_pr.ix[index, 'date'][i] = [datetime.strptime(grouped_pr.ix[index,'date'][i], '%m %d, %Y').date().toordinal()]
        grouped_pr.ix[index, 'date'].sort()
        date = np.array(grouped_pr.ix[index, 'date'])
        kde = KernelDensity(kernel='gaussian', bandwidth=1).fit(date)
        kde_list.append(kde.score_samples(date))
    sorted_by_max_of_each_row = pd.DataFrame()
    kde_df = (pd.DataFrame(kde_list)).transpose()
    kde_df.columns = p_id

    kde_df['max'] = kde_df.max(axis = 1)
    sorted_by_max_of_each_row = kde_df.sort_values(by='max', ascending=False, inplace=False).reset_index(drop=True)
    threshold = sorted_by_max_of_each_row['max'][len(sorted_by_max_of_each_row['max'])/2] #threshold is the top 50th value
    kde_df.drop('max', axis=1, inplace=True)

    intersection = []
    for product_kde in kde_df:
        temp_df = kde_df[kde_df[product_kde]>threshold][product_kde]
        intersection.append(temp_df.index.tolist())

    df_indices = (pd.DataFrame(intersection )).transpose()
    df_indices.columns = p_id

    grouped_pr['bursts'] = grouped_pr['date']
    for column in df_indices:
        b = []
        a = pd.to_numeric(df_indices[column].dropna())
        if (len(a) == 0):
            grouped_pr.ix[column, 'bursts'] = []
            continue
        ini = a[0]
        for i in range(len(a)):

            if (i is (len(a) - 1)) :
                b.append([grouped_pr.ix[column,"date"][int(ini)],grouped_pr.ix[column,"date"][int(a[i])]])

            elif ((int(a[i]+1) is not int(a[i+1]))):
                b.append([grouped_pr.ix[column,"date"][int(ini)],grouped_pr.ix[column,"date"][int(a[i])]])
                ini = a[i+1]

        grouped_pr.ix[column,'bursts'] = b

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

