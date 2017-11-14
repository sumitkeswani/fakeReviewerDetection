'''
This file can be used ot convert a json dataset file to a pandas df
and further to a csv file
'''

import pandas
import json
import pandas as pd
import gzip

file_name = "./reviews_Books_5.json"
csv_file = "./reviews_books.csv"
def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

df = getDF(file_name)
df.to_csv(csv_file, sep="\t")

















