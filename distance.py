from features import *


# Common List of Products
def heurtistic_1(reviewers_df):
    count_common_products = productFeature(reviewers_df)
    count_common_products.columns = ["reviewer_1", "reviewer_2", "h_1"]
    return count_common_products

# Cosine Similarity
def heurtistic_2(reviewers_df):
    reviewers_df.reset_index(level=0, inplace=True)
    rowiter = reviewers_df.iterrows()
    similarity_list = []
    for index_reviewer1, row_reviewer1 in rowiter:
        nextrowiter = reviewers_df.iloc[index_reviewer1 + 1:, :].iterrows()
        for index_reviewer2, row_reviewer2 in nextrowiter:
            AB = reviewers_df.ix[index_reviewer1,'burst_ratio'] * reviewers_df.ix[index_reviewer2,'burst_ratio'] \
            + reviewers_df.ix[index_reviewer1, 'similarity_index'] * reviewers_df.ix[index_reviewer2, 'similarity_index'] \
            + reviewers_df.ix[index_reviewer1,'rating_deviation'] * reviewers_df.ix[index_reviewer2,'rating_deviation'] \
            + reviewers_df.ix[index_reviewer1,'avg_helpfulness'] * reviewers_df.ix[index_reviewer2,'avg_helpfulness']

            A = reviewers_df.ix[index_reviewer1,'burst_ratio']**2 + reviewers_df.ix[index_reviewer1,'rating_deviation']**2 \
                + reviewers_df.ix[index_reviewer1, 'similarity_index']**2 + reviewers_df.ix[index_reviewer1,'avg_helpfulness']**2

            B = reviewers_df.ix[index_reviewer2, 'burst_ratio']**2 + reviewers_df.ix[index_reviewer2, 'rating_deviation']**2 \
                + reviewers_df.ix[index_reviewer2, 'similarity_index']**2 + reviewers_df.ix[index_reviewer2, 'avg_helpfulness']**2

            reviwer_pair = []
            reviwer_pair.append(row_reviewer1['reviewerID'])
            reviwer_pair.append(row_reviewer2['reviewerID'])
            reviwer_pair.append(AB / (A ** 0.5) * (B ** 0.5))
            similarity_list.append(reviwer_pair)

    graph_df['similarity'] = pd.DataFrame(similarity_list)
    return graph_df


# Common Burst Time
def heurtistic_3():
    pass

def compute_distance(reviewers_df):
    #graph_df with reviewer_1, reviewer_2 and h_1 added
    # graph_df = heurtistic_1(reviewers_df)
    graph_df = heurtistic_2(reviewers_df)


if __name__ == '__main__':
    reviewers_df = compute_features()
    graph_df = compute_distance(reviewers_df)
    print graph_df
