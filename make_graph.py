import pandas as pd
import json


'''
This script generates an output json file for plotting visualizations
It takes the similirity distances file and BP truthfulness values of each reviewer, joins on the two tables,
and then converts it to csv.
'''
def main():
    bp = pd.DataFrame.from_csv("./output.csv", sep=",")
    bp["reviewer_id"] = bp["reviewer_id"].apply(lambda x: x.strip())
    filtered = pd.DataFrame.from_csv("./filtered_music_data.csv", sep=",")
    final = pd.merge(filtered, bp, how='left', right_on=['reviewer_id'], left_on=["reviewer_1"])
    final.columns = [u'reviewer_1', u'reviewer_2', u'common_products', u'common_bursts', u'numerical_similarity', u'final_distance', u'reviewer_id', 'T_reviewer_1']
    final = pd.merge(final, bp, how='left', right_on=['reviewer_id'], left_on=["reviewer_2"])
    final.columns = [u'reviewer_1', u'reviewer_2', u'common_products', u'common_bursts', u'numerical_similarity', u'final_distance', u'reviewer_id_x', 'T_reviewer_1', 'reviewer_id_y', 'T_reviewer_2']
    fp = open('./demo/demo.json', 'w')
    fp.write(final.to_json(orient='records'))
    fp.close()
    #final.to_csv("/Users/mugdha_bondre/Documents/DVA/DVA Project//fakeReviewerDetection/joined_music_data_new.csv", ',')


if __name__ == '__main__':
    main()


