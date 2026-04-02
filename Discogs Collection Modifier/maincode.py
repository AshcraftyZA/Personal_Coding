import pandas as pd

df= pd.read_csv("/workspaces/Personal_Coding/Discogs Collection Modifier/zackdimondrecords1-collection-20260402-1501.csv")
backup = df
df_stock = df.dropna(subset =['Collection Notes'])
df_sold = df[df['Collection Notes'].isna()]
df_sold['Blank'] = ''
df_sold =df_sold[['Blank','Artist', 'Title', 'CollectionFolder','Collection Price','Collection Sold Price','Date Added']]
df_sold['CollectionFolder']=df_sold['CollectionFolder'].replace('Uncategorized', 'Individual Find')
today = pd.Timestamp.today().normalize()
df_sold['Date Added'] = pd.to_datetime(df_sold['Date Added'])
df_sold.loc[
    df_sold['CollectionFolder'] == 'Individual Find',
    'CollectionFolder'
] = (today - df_sold['Date Added']).dt.days.astype(str)
df_sold['Collection Price'] = df_sold['Collection Price'].fillna(3)
df_sold['Collection Sold Price'] = df_sold['Collection Sold Price'].fillna(df_sold['Collection Price'])
df_sold=df_sold[['Blank','Artist', 'Title', 'CollectionFolder', 'Collection Price', 'Collection Sold Price']]
df_stock= df_stock[['Artist', 'Title','Collection Price']]
df_stock['Collection Price']= df_stock['Collection Price'].fillna(3)


while True:
    userin = int(input("Enter a number. If want the sold list, click 1. If you want the back up, click 2. If you want the stock invetory, click 3 If you want to end, click 0 "))
    if userin == 1:
        df_sold.to_csv("Sold.csv", index=False)
    if userin == 2:
        backup.to_csv("Backup.csv", index =False)
    if userin == 3:
        df_stock.to_csv("Stock.csv", index= False)
    if userin == 0:
        break
