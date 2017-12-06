'''
This file will be used to calculate features for a reviewer
'''

import pandas as pd
from collections import defaultdict
from sklearn.neighbors.kde import KernelDensity
import numpy as np
from datetime import datetime
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
from scipy.stats import norm

average = lambda n : sum(n) / len(n)
average2 = lambda n : sum(n) / len(n) if len(n) > 0 else 0

def kde(grouped_df):
    product_ratings_list = []

    #Grouping ratings and dates by product ID
    for index, row in grouped_df.iterrows():
        for index_list, val in enumerate(row['asin']):
            product_ratings_list.append([val, grouped_df.ix[index,'overall'][index_list], grouped_df.ix[index,'reviewTime'][index_list]])
    product_ratings = pd.DataFrame(product_ratings_list, columns=["product_id", "rating", "date"])
    grouped_pr = pd.DataFrame(columns=product_ratings.columns.values)
    grouped_pr["rating"] = product_ratings.groupby("product_id")["rating"].apply(list)
    grouped_pr["date"] = product_ratings.groupby("product_id")["date"].apply(list)

    #Deleting product_id row as it's already indexed on product_id
    grouped_pr.drop('product_id', axis=1, inplace=True)


    #Now grouped_pr contains product_id, [list of ratings], [list of dates]

    kde_list = []
    p_id = []

    count = 0
    # Calculating kde for all dates in all products
    for index, row in grouped_pr.iterrows():
        p_id.append(index)
        for i in range(len(grouped_pr.ix[index,'date'])):
            #Changing date to ordinal format as kde accepts numerical values only
            grouped_pr.ix[index, 'date'][i] = [datetime.strptime(grouped_pr.ix[index,'date'][i], '%m %d, %Y').date().toordinal()]
        grouped_pr.ix[index, 'date'].sort()
        date = np.array(grouped_pr.ix[index, 'date'])
        #Fittind KDE
        kde = KernelDensity(kernel='gaussian', bandwidth=1).fit(date)
        log_dens = kde.score_samples(date)
        kde_list.append(log_dens)

        if count == 1000:
            print "Plotting"
            ax = pd.DataFrame(np.array(grouped_pr.ix[index, 'date'])).plot.kde(title="KDE Plot", legend=False)
            ax.set_xlabel("Unixtime")
            ax.set_ylabel("Density")
            plt.show()

        count += 1


    #Converting to dataframe : Each columns is a product_id with list of kdes for each sorted date
    kde_df = (pd.DataFrame(kde_list)).transpose()
    kde_df.columns = p_id

    #Computing threshold
    kde_df['max'] = kde_df.max(axis = 1)
    sorted_by_max_of_each_row = pd.DataFrame()
    sorted_by_max_of_each_row = kde_df.sort_values(by='max', ascending=False, inplace=False).reset_index(drop=True)
    threshold = sorted_by_max_of_each_row['max'][len(sorted_by_max_of_each_row['max'])/2] #threshold is the top 50th value
    kde_df.drop('max', axis=1, inplace=True)

    #Filtering all indices with kde > threshold for each product
    intersection = []
    for product_kde in kde_df:
        temp_df = kde_df[kde_df[product_kde]>threshold][product_kde]
        intersection.append(temp_df.index.tolist())

    df_indices = (pd.DataFrame(intersection )).transpose()
    df_indices.columns = p_id

    # Computing burst periods (pair of dates on x-axis where kde was above threshold)
    grouped_pr['bursts'] = grouped_pr['date']
    for column in df_indices:
        b = []
        b_id = []
        id = 0
        a = pd.to_numeric(df_indices[column].dropna())
        if (len(a) == 0):
            grouped_pr.ix[column, 'bursts'] = []
            continue
        ini = a[0]
        for i in range(len(a)):

            if (i is (len(a) - 1)) :
                b.append([grouped_pr.ix[column,"date"][int(ini)],grouped_pr.ix[column,"date"][int(a[i])]])
                b_id.append(column + '-' + str(id))
                id += 1

            elif ((int(a[i]+1) is not int(a[i+1]))):
                b.append([grouped_pr.ix[column,"date"][int(ini)],grouped_pr.ix[column,"date"][int(a[i])]])
                b_id.append(column + '-' + str(id))
                id += 1
                ini = a[i+1]

        grouped_pr.ix[column,'bursts'] = b
        grouped_pr.ix[column, 'bursts_ids'] = b_id
    return grouped_pr

def reviewer_bursts(grouped_df, grouped_pr):
    #Adding ordinal column
    prods_df = grouped_df[['asin', 'reviewTime']]
    date_conv = lambda row: [datetime.strptime(r, '%m %d, %Y').date().toordinal() for r in row.reviewTime]
    prods_df['ordinal'] = prods_df.apply(date_conv, axis=1)
    prod_df = prods_df.drop('reviewTime', axis=1)
    prods_df = prods_df.reset_index()

    grouped_pr = grouped_pr.drop(['rating', 'date'], axis=1)
    calc_count = lambda row: sum([sum([1 for b in grouped_pr['bursts'][prod] if o_time >= b[0][0] and o_time <= b[1][0]]) \
                                if grouped_pr['bursts'].get(prod) else 0 \
                                for prod, o_time in zip(row.asin,row.ordinal)])

    #TODO: @Mugdha please verify the code below
    bursts = lambda row: filter(None, ([next((b_id for b, b_id \
                        in zip(grouped_pr['bursts'][prod], grouped_pr['bursts_ids'][prod]) \
                        if o_time >= b[0][0] and o_time <= b[1][0]), None) \
                        if grouped_pr['bursts'].get(prod) else None for prod, o_time in zip(row.asin,row.ordinal)]))
    prods_df['burst_ids'] = prods_df.apply(bursts, axis=1)
    prods_df['burst_count'] = prods_df.apply(calc_count, axis=1)

    return prods_df

def burst_ratio(prods_df):
    find_burst = lambda row: float(row['burst_count'])/len(row.ordinal)
    prods_df['burst_ratio'] = prods_df.apply(find_burst, axis=1)
    prods_df = prods_df.set_index('reviewerID')
    return prods_df


def productFeature(gdf):
    prodf= gdf['asin'].to_frame()
    prodf.reset_index(level=0, inplace=True)
    rowiter=prodf.iterrows()
    total=[]
    for index,row in rowiter:
        nextrowiter=prodf.iloc[index+1:,:].iterrows()
        for index1,row1 in nextrowiter:
            commonelem=list(set(row['asin']).intersection(set(row1['asin'])))
            commelemlist=[]
            commelemlist.append(row['reviewerID'])
            commelemlist.append(row1['reviewerID'])
            commelemlist.append(len(list(commonelem)))#,commonelem[0])
            total.append(commelemlist)
    pdf=pd.DataFrame(total)
    return pdf



#creates a seperate column "rating_deviation" in df_grouped - saves the rating deviation for each reviewer
def rating_deviation(grouped_df):
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

def text_similarity(grouped_df):
    reviews_df  = grouped_df['summary'].to_frame()
    sim =  lambda row: average2([SequenceMatcher(None, r1, r2).ratio() for r1 in row.summary for r2 in row.summary\
                        if r1 != r2])
    reviews_df['similarity_index'] = reviews_df.apply(sim, axis =1)
    grouped_df['similarity_index'] = reviews_df['similarity_index']

    return grouped_df

# Pranathi's code
def average_helpfulness(grouped_df):
    for index, reviewer in grouped_df.iterrows():
        # print grouped_df.index[i]
        numer = 0.0
        denom = 0.0
        for review in reviewer["helpful"]:
            nums = review.split(",")
            numer += int(nums[0][1:])
            denom += int(nums[1][:-1])
        if denom <= 1:
            avg_helpfulness = 0.0
        else:
            avg_helpfulness = numer/denom
        grouped_df.ix[index, 'avg_helpfulness'] = avg_helpfulness

    return grouped_df

def compute_features():
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

    # Reviewer ID not needed as it is in index
    grouped_df.drop('reviewerID', axis=1, inplace=True)

    #grouped_df = grouped_df[:6000]

    print "Calculating rating deviation"
    # Feature 1: Rating Deviation
    # grouped_df = rating_deviation(grouped_df)

    print "Calculating Burst Review ratio"
    # Feature 2: Burst Review Ratio
    grouped_pr = kde(grouped_df)
    prods_df = reviewer_bursts(grouped_df, grouped_pr)

    prods_df = burst_ratio(prods_df)
    grouped_df['burst_ratio'] = prods_df['burst_ratio']
    grouped_df['burst_ids'] = prods_df['burst_ids']

    print "Calculating text similarity"
    # Feature 3: Text Similarity
    grouped_df = text_similarity(grouped_df)

    # Feature 4: List of products : grouped_df["products"]

    print "calculating Average helpfulness"
    # Feature 5: Average helpfulness
    grouped_df = average_helpfulness(grouped_df)

    # Feature 6: Burst Time Frames

    # print grouped_df['reviewerID', 'asin', 'rating_deviation', 'burst_ratio', 'similarity_index', 'avg_helpfulness']
    return grouped_df


if __name__ == '__main__':
    compute_features()
