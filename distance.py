from features import *

# Common List of Products
def heurtistic_1(reviewers_df):
    count_common_products = productFeature(reviewers_df)
    count_common_products.columns = ["reviewer_1", "reviewer_2", "h_1"]
    return count_common_products

# Cosine Similarity
def heurtistic_2(reviewers_df):
    pass

# Common Burst Time
def heurtistic_3():
    pass

def compute_distance(reviewers_df):
    #graph_df with reviewer_1, reviewer_2 and h_1 added
    graph_df = heurtistic_1(reviewers_df)

if __name__ == '__main__':
    pass