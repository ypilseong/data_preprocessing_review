
import pandas as pd

df = pd.read_csv('data/uniqe_store_data.csv', sep=',', encoding='utf-8', index_col=0)
df.reset_index(drop=True,inplace=True)
df.drop(df.columns[0], axis=1, inplace=True)
df.to_csv('data/unique_store_data.csv', encoding='utf-8')