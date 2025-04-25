import pandas as pd

df = pd.read_csv('./source/products.tsv', delimiter='\t')
df.drop(columns=['asin', 'discontinued', 'title', 'categories', 'salesrank', 'similars_count', 'avg_rating', 'total_reviews', 'downloaded_reviews'], inplace=True)
df.to_csv('./gephi/products.csv', index=False)