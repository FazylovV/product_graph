import pandas as pd
import matplotlib.pyplot as plt

products = pd.read_csv('../data/products.tsv', delimiter='\t')
print(products['group_name'].value_counts())
