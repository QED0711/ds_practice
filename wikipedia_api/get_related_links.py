import requests
from bs4 import BeautifulSoup


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
    
      
def get_related_links(url):
    resp = requests.get(url)
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