import pandas as pd
from WikiScrapper import *

def run():
    titles_df = pd.read_csv("top_wikipedia_articles.csv")

    for i in range(titles_df.shape[0]):
        current = titles_df.iloc[i]
        
        if current.visited == 0:
            
            print(current['title'])
            
            title = current.title
            
            scrapper = WikiScrapper()
            try:
                scrapper.traverse_from("https://en.wikipedia.org/wiki/{}".format(title), max_depth=3, max_nodes=None)
                scrapper.to_mlab()
            except:
                pass
                
            titles_df.iloc[i,1] = 1
            titles_df.to_csv("top_wikipedia_articles.csv", index=False)
        
            time.sleep(2)


if __name__ == "__main__":
    run()




