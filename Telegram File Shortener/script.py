import os
import json
import pymongo
import requests
from utils import random_post, aeshash


if not os.path.exists("posts.json"):
    url = "https://harshcoderz.blogspot.com/feeds/posts/summary?alt=json-in-script"
    r = requests.get(url)
    data = r.text
    json_data = data.strip('gdata.io.handleScriptLoaded(').strip(');')
    with open("posts.json", "w") as file:
        json.dump(json_data, file)

try:
    f = open("posts.json", "r")
    json_data = json.load(f)
    json_data = json.loads(json_data)
    content = json_data["feed"]["entry"]

    DATABASE_URI = "mongodb+srv://harshsoni:harshsoni@cluster0.cdvqw1h.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(DATABASE_URI)
    database = client['Cluster0']
    collection = database['files_data_store']
    result = collection.find()

    count = 0
    for document in result:
        random_post_link = random_post(content)
        _id = document['_id']
        shorten_link = aeshash(random_post_link, _id)

        updated_document = {"$set": {"file_link": shorten_link}}
        result = collection.update_one(document, updated_document)

        count += 1
        print(f"{count} files updated")
        
except Exception as e:
    print(e)