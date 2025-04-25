import pandas as pd

df = pd.read_csv('./data/categories.csv')
df.drop_duplicates(inplace=True)
df.to_csv('./data/categories.csv', index=False)