import pandas as pd

df= pd.read_csv("/workspaces/Personal_Coding/Discogs Collection Modifier/zackdimondrecords1-collection-20260402-0546.csv")
backup = df
df2 = df.dropna(subset =['Collection Notes'])
df_nulls = df[df['Collection Notes'].isna()]
df_nulls['Blank'] = ''
df_nulls =df_nulls[['Blank','Artist', 'Title', 'CollectionFolder']]