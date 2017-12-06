from features import *


# TODO : Distance should be 1 - computation as higher values of heuristics indicate closeness,

# Cosine Similarity
def heurtistics(reviewers_df):
    reviewers_df.reset_index(inplace = True)
    rowiter = reviewers_df.iterrows()
    similarity_list = []
    total = []
    for index_reviewer1, row_reviewer1 in rowiter:
        nextrowiter = reviewers_df.iloc[index_reviewer1 + 1:, :].iterrows()
        for index_reviewer2, row_reviewer2 in nextrowiter:
            try:
                commonelem = list(set(row_reviewer1['asin']).intersection(set(row_reviewer2['asin'])))
                unionelem = list(set(row_reviewer1['asin']).union(set(row_reviewer2['asin'])))
                commonelem_burst = list(set(row_reviewer1['burst_ids']).intersection(set(row_reviewer2['burst_ids'])))
                unionelem_burst = list(set(row_reviewer1['burst_ids']).union(set(row_reviewer2['burst_ids'])))
                reviwer_pair = []
                reviwer_pair.append(row_reviewer1['reviewerID'])
                reviwer_pair.append(row_reviewer2['reviewerID'])
                if len(unionelem):
                    reviwer_pair.append(float(len(list(commonelem)))/len(unionelem))  # ,commonelem[0])
                else:
                    reviwer_pair.append(0)
                if len(unionelem_burst):
                    reviwer_pair.append(float(len(list(commonelem_burst)))/len(unionelem_burst))
                else:
                    reviwer_pair.append(0)
            except:
                import pdb; pdb.set_trace()

            AB = reviewers_df.ix[index_reviewer1,'burst_ratio'] * reviewers_df.ix[index_reviewer2,'burst_ratio'] \
            + reviewers_df.ix[index_reviewer1, 'similarity_index'] * reviewers_df.ix[index_reviewer2, 'similarity_index'] \
            + reviewers_df.ix[index_reviewer1,'rating_deviation'] * reviewers_df.ix[index_reviewer2,'rating_deviation'] \
            + reviewers_df.ix[index_reviewer1,'avg_helpfulness'] * reviewers_df.ix[index_reviewer2,'avg_helpfulness']

            A = reviewers_df.ix[index_reviewer1,'burst_ratio']**2 + reviewers_df.ix[index_reviewer1,'rating_deviation']**2 \
                + reviewers_df.ix[index_reviewer1, 'similarity_index']**2 + reviewers_df.ix[index_reviewer1,'avg_helpfulness']**2


            B = reviewers_df.ix[index_reviewer2, 'burst_ratio']**2 + reviewers_df.ix[index_reviewer2, 'rating_deviation']**2 \
                + reviewers_df.ix[index_reviewer2, 'similarity_index']**2 + reviewers_df.ix[index_reviewer2, 'avg_helpfulness']**2

            reviwer_pair.append(AB / ((A ** 0.5) * (B ** 0.5)))
            similarity_list.append(reviwer_pair)

    graph_df = pd.DataFrame(similarity_list)
    graph_df.columns = ['reviewer_1', 'reviewer_2', 'common_products', 'common_bursts', 'numerical_similarity' ]
    return graph_df


def compute_distance(reviewers_df, alpha, beta, gamma):
    #graph_df with reviewer_1, reviewer_2 and h_1 added
    graph_df = heurtistics(reviewers_df)
    graph_df['final_distance'] = ((alpha * graph_df['common_products']) + \
                                  (beta * graph_df['common_bursts']) + \
                                  (gamma * graph_df['numerical_similarity'])) / (alpha + beta + gamma)
    return graph_df


if __name__ == '__main__':
    reviewers_df = compute_features()
    graph_df = compute_distance(reviewers_df, 1, 1, 1)
    graph_df.to_csv('./distances.csv', sep = '\t')
