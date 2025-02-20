from pymongo import MongoClient
import json
import pandas as pd
from upload_to_gdrive import upload_json_to_gdrive

client = MongoClient()
db = client['advpos-react']
coll_names = db.list_collection_names()
coll_name_select = input(f"select collection to backup from the list {coll_names}")
print(f"you have selected {coll_name_select}. starting to generate json now")

docs = list(db[coll_name_select].find({}, {"_id": 0}))
new_docs = []
for i in docs:
    try:
        if coll_name_select == "accounts":
            i['subscription_expiration'] = pd.to_datetime(i['subscription_expiration']).strftime("%Y-%m-%d %H:%M:%S")
            i['date_added'] = pd.to_datetime(i['date_added']).strftime("%Y-%m-%d %H:%M:%S")
        elif coll_name_select == "cash_flows":
            i['date_added'] = pd.to_datetime(i['date_added']).strftime("%Y-%m-%d %H:%M:%S")
            i['date_of_transaction'] = pd.to_datetime(i['date_of_transaction']).strftime("%Y-%m-%d %H:%M:%S")
        elif coll_name_select in ["expenses", "planners"]:
            i['date_added'] = pd.to_datetime(i['date_added']).strftime("%Y-%m-%d %H:%M:%S")
        if i.get('date_updated'):
            i['date_updated'] = pd.to_datetime(i['date_updated']).strftime("%Y-%m-%d %H:%M:%S")
        new_docs.append(i)
    except TypeError as e:
        print(e)
        new_docs.append(i)

with open(f"{coll_name_select}.json", 'w') as file:
    json.dump(new_docs, file, indent=4)

print(f"{coll_name_select}.json saved")
print(f"now uploading {coll_name_select}.json to gdrive")

upload_json_to_gdrive(f"{coll_name_select}.json")
