import pandas as pd
import numpy as np


groups = {}
with open('./data/groups.csv', 'r', encoding='utf-8') as file:
    file.readline()
    for line in file:
        parts = line.replace('\n', '').split(',')
        groups[parts[1]] = int(parts[0])

df = pd.read_csv('./data/products.tsv', delimiter='\t')
# df = df[df['discontinued'] != True]
# print(df.info())
print(groups)

df['group_id'] = df['group_name'].map(groups)
df = df.convert_dtypes()
df.drop('group_name', axis=1, inplace=True)
df = df[['id', 'asin', 'discontinued',
       'group_id', 'title', 'categories', 'salesrank',
       'similars_count', 'avg_rating', 'total_reviews', 'downloaded_reviews']]
df.to_csv('./data/product_groupid.tsv', sep='\t', index=False)

