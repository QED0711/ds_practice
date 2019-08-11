
import pandas as pd
import pymongo
from keys import *

def mlab_to_csv():
    uri = f"mongodb://{mlab_api['username']}:{mlab_api['password']}@ds261277.mlab.com:61277/wiki_scrapper"
    client = pymongo.MongoClient(uri)

    db = client.get_default_database()

    data_fetcher = db["known_related"]

    mlab_data = data_fetcher.find({})
    
    docs = []

    for doc in mlab_data:
        docs.append((doc["title"], doc["url"], doc["links"]))

    pd.DataFrame(docs, columns=["title", "url", "links"]).to_csv("labeled_data.csv", index=False)

    
if __name__ == "__main__":
    mlab_to_csv()