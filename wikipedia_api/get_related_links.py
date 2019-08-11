import requests
from bs4 import BeautifulSoup
import signal

# signal timout #
def signal_timeout_handler():
    print("Timeout")
    raise OSError("Took Too Long")

signal.signal(signal.SIGALRM, signal_timeout_handler)




def find_see_also(soup):
    return soup.find(attrs={"id":"See_also"})


def find_links(soup):
    if soup.name == "ul":
        return soup.find_all("li")
    
    if soup.name == "div" and " ".join(soup["class"]) == "div-col columns column-width":
        return soup.find_all("li")
    
    return find_links(soup.find_next_sibling())


def process_links(links):
    hrefs = []
    for link in links:
        hrefs.append("https://en.wikipedia.org" + link.find('a').get("href"))
    return tuple(hrefs)
    
    
    
def get_article_title(soup):
    return soup.find(attrs={"id":"firstHeading"}).text
    
      
def get_related_links(url, timeout=5):
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
    try:
        signal.alarm(timeout)
        resp = requests.get(url, headers={"User-Agent": user_agent})
        signal.alarm(0)
    except:
        return None

    soup = BeautifulSoup(resp.content, "html.parser")
    
    title = get_article_title(soup)
    
    see_also = find_see_also(soup)
    
    if see_also:
        links = find_links(see_also.find_parent())
    else: 
        return None
    
    return {
        "title": title,
        "url": url,
        "links": process_links(links)
    }