import pandas as pd
import pymongo
from copy import copy, deepcopy
import pdb

from keys import *

from get_related_links import get_related_links
import time

import signal

class WikiScrapper:
    
    def __init__(self):
        self.data = []
    
    
    def traverse_from(self, url, max_depth=3, max_nodes=100):
        current = get_related_links(url)
        
        
        if current:
            queue = [link for link in current['links'] if self.valid_url(link)]
        else: 
            return

        self.data = [current]
        seen = {current["title"]: True}
        depth_count = 1

        while depth_count < max_depth and len(queue) > 0:
            queue_copy = queue.copy()
            
            for link in queue_copy:
                try:
                    current_url = queue.pop(0)
                    current = get_related_links(current_url)

                    if current:
                        print(current["title"] + "" * 50, end="\r", flush=True)
                        if seen.get(current['title']):
                            continue
                        
                        seen[current['title']] = True
                        
                        queue += current['links']
                        self.data.append(current)

                        if max_nodes and len(self.data) == max_nodes:
                            return self.data
                except:
                    continue
            
            depth_count += 1
            
        return self.data
        
    def valid_url(self, url):
        return len(url.split("//")) <= 2

    def to_dataframe(self):
        return pd.DataFrame(self.data)
    
    def to_csv(self, file_name):
        self.to_dataframe().to_csv(file_name, index=False)
    
    def add_ids(self):
        data = deepcopy(self.data)
        
        for article in data:
            article['_id'] = article['title']
        return data
    
    def to_mlab(self):
        
        uri = f"mongodb://{mlab_api['username']}:{mlab_api['password']}@ds261277.mlab.com:61277/wiki_scrapper"
        client = pymongo.MongoClient(uri)

        db = client.get_default_database()

        data_inserter = db["known_related"]
        
        # add ids to our data for so we don't save duplicates of the same topic
        # save to a new version so that we don't overwrite any of our other data
        links_data = self.add_ids()

        for article in links_data:
            try:
                data_inserter.insert_one(article)
            except:
                continue

        client.close()


if __name__ == "__main__":
    scrapper = WikiScrapper()
    scrapper.traverse_from("https://en.wikipedia.org/wiki/Brain", max_depth=3, max_nodes=2)
    print(scrapper.data)