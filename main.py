'''
Main function of the code
'''
from features import *
from distance import *

if __name__ == '__main__':
    reviewers_df = compute_features()
    # graph_def = distance(reviewers_df)

    # reviewer_1      reviewer_2      h_1     h_2     h_3     distance
