from pymongo import MongoClient
from dotenv import load_dotenv
import os
from tqdm import tqdm
from bson import ObjectId
from datetime import datetime

load_dotenv()
mongodb_uri_ec2 = os.getenv("MONGODB_URI_EC2")
mongodb_uri_server = os.getenv("MONGODB_URI_SERVER")
client = MongoClient(mongodb_uri_ec2)
local_client = MongoClient(mongodb_uri_server)

dbs = client.list_database_names()
dbs_exceptions = ['Christina', 'admin', 'config', 'local']

new_dbs = []
for i in dbs:
    if not i in dbs_exceptions:
        new_dbs.append(i)
print(new_dbs)

logs = []
for i in tqdm(new_dbs, total=len(new_dbs), ncols=100):
    db_local = local_client[i]
    db_ec2 = client[i]
    for x in db_ec2.list_collection_names():
        coll_ec2 = db_ec2[x]
        coll_local = db_local[x]
        docs_ec2 = list(coll_ec2.find())
        upserted = 0
        modified = 0
        for z in docs_ec2:
            primary_fields = {
                "date_synched": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            primary_fields.update(z)
            if i == 'about_the_dev':
                result = coll_local.update_one({"_id": primary_fields['_id']}, {"$set": primary_fields}, upsert=True)
            else:
                result = coll_local.update_one({"_id": ObjectId(primary_fields['_id'])}, {"$set": primary_fields}, upsert=True)
            if result.upserted_id:
                upserted += 1
            elif result.modified_count:
                modified += 1
    print(f"Backup log: modified: {modified} in {coll_local.name}")
    print(f"Backup log: upserted: {upserted} in {coll_local.name}")
    logs.append({
        "date_logged": datetime.now(),
        "modified": f"Backup log: modified: {modified} in {coll_local.name}",
        "upserted": f"Backup log: upserted: {upserted} in {coll_local.name}",
    })

coll_log = db_local['backup_logs']
coll_log.insert_many(logs)
print("finished workflow")