import pandas as pd
from datetime import date
import discogs_client
import requests
import json
import time

df= pd.read_csv("/workspaces/Personal_Coding/Discogs Collection Modifier/zackdimondrecords1-collection-20260413-2024.csv")
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
    userin = int(input("Enter a number. \n If want the sold list, click 1.\n If you want the back up, click 2. \n If you want the stock invetory, click 3. \n If you want to delete the old inventory, click 4. \n If you want to end, click 0 "))
    if userin == 1:
        df_sold.to_csv("Sold.csv", index=False)
    if userin == 2:
        backup.to_csv("Backup.csv", index =False)
    if userin == 3:
        df_stock.to_csv("Stock.csv", index= False)
    if userin == 4:
        username='ZackDimondRecords1'
        folder_id=1
        headers = {
            "User-Agent": "Inventory_Remover_ZDR",
            "Authorization": "Discogs token=ONQcVBLePsQvGKasmFsIdIdEsKmkvOxKVwntWgdZ"
        }
        page = 1
        per_page = 50
        folder_id = 0
        collection_url = f"https://api.discogs.com/users/{username}/collection/folders/{folder_id}/releases?page={page}&per_page={per_page}"
        response = requests.get(collection_url, headers=headers)
        data = response.json()
        pages_n = response.json()['pagination']['pages']
        var_page = 0
        delete_list = []
        true_counter = 0
        while var_page < pages_n:
            var_page += 1
            var_url = f"https://api.discogs.com/users/{username}/collection/folders/{folder_id}/releases?page={var_page}&per_page={per_page}"
            var_response = requests.get(var_url, headers=headers)
            if var_response.status_code != 200:
                print(f"Error {var_response.status_code}")
                continue
            var_json = var_response.json()
            releases = var_json.get('releases', [])
            for release in releases:
                notes = release.get("notes") or []
                if len(notes) > 0 and notes[0].get("value") == "A":
                    true_counter += 1
                if any(n.get("field_id") == 5 for n in notes):
                    delete_list.append({
                        "folder_id": release["folder_id"],
                        "release_id": release["id"],
                        "instance_id": release["instance_id"]
                    })
            for item in delete_list:
                url = f"https://api.discogs.com/users/{username}/collection/folders/{item['folder_id']}/releases/{item['release_id']}/instances/{item['instance_id']}"
                response = requests.delete(url, headers=headers)
                #AI helped me to figure out delete codes and testing stuff. 
                if response.status_code == 204:
                    print("✅ Deleted")
                elif response.status_code == 429:
                    print("⏳ Rate limited — sleeping...")
                    time.sleep(10)
                    continue
                else:
                    time.sleep(1.5) 
    if userin == 0:
        break
