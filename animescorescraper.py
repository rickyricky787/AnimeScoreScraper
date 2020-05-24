# Anime Ranking Search using BeautifulSoup
# Author: Ricky Rodriguez

import requests
from bs4 import BeautifulSoup
import re

# A class that will contain all the data we are looking for; used by functions

class Data:
    def __int__(self, title = "None", score = 0.0, conv_score = 0.0, votes = 0.0, link = "None", image = "None"):
        self.title = title
        self.score = score
        self.conv_score = conv_score
        self.votes = votes
        self.link = link
        self.image = image


# Def: Finds the link of the anime webpage in a website (MyAnimeList, Anime Planet, Anilist)
# Input: User inputed "name", "keyword" and "website" of the webpage we plan on scraping
# Output: The link of the anime webpage (if found), "None" (if not found)

def getLink(name, keyword, website):

    # Function will "google" the anime name, followed by the keyword (ex. Pokemon + MyAnimeList).
    search = name + " " + keyword
    page = requests.get("https://www.google.com/search?q={}&num={}".format(search, 5))
    soup = BeautifulSoup(page.content, "html5lib")
    links = soup.findAll("a")
 
    # "links" has first 5 websites found from Google
    # "search_results" will (hopefully) have the link we want
    search_results = "None"

    for link in links :
        link_href = link.get("href")
        # If not an image (imgurl) or a snippet (?sa=X), add link to array
        if website in link_href and not "imgurl" in link_href and not "?sa=X" in link_href:
            search_results = link.get("href").split("?q=")[1].split("&sa=U")[0]
            break

    return search_results

# To get data from MyAnimeList
def MyAnimeList(name):
    results = Data()
    results.link = getLink(name, "MyAnimeList", "myanimelist.net/anime")
    if results.link != "None":
        page = requests.get(results.link)
        soup = BeautifulSoup(page.content, "html5lib") # "soup" means the WHOLE html code
        element_check = soup.select_one("div.fl-l.score") # If element_check is none, then no anime webpage exist
        if element_check is not None:
            container = element_check
            results.score = container.get_text()
            results.score = results.score.strip()

            if results.score != "N/A":  # An upcoming anime has an "N/A" rating
                results.score = float(results.score)
                results.conv_score = float(results.score) * 10

            container = soup.find("span", {"itemprop":"ratingCount"})
            if container is not None:
                results.votes = container.get_text()
                results.votes = float(results.votes)
            else:
                results.votes = "N/A"

            results.title = soup.find("span", {"class":"h1-title"})
            results.title = results.title.get_text()

            results.image = soup.find("img", {"itemprop":"image"})
            results.image = str(results.image)
            results.image = results.image.split('data-src="')[1].split('" ')[0]
            
        else:
            # If there is no "fl-l.score", then link is incorrect / anime webpage not found
            results.link = "None"
            results.score = 0.0
            results.conv_score = 0.0
            results.votes = 0.0
            results.title = "None"
            results.link = "None"
    else:
        # If no link was returned from getLink(), then anime webpage not found
        # results.link is already setto "None"
        results.score = 0.0
        results.conv_score = 0.0
        results.votes = 0.0
        results.title = "None"
        results.image = "None"
    return results

# To get data from AnimePlanet
def AnimePlanet(name):
    results = Data()
    results.link = getLink(name, "Anime Planet", "anime-planet.com/anime")
    if results.link != "None":
        page = requests.get(results.link)
        soup = BeautifulSoup(page.content, "html5lib")
        element_check = soup.select_one("div.avgRating")
        if element_check is not None:
            container = element_check
            results.score = container.span["style"]
            results.score = results.score[7:-1]
            results.score = float(results.score)
            results.conv_score = results.score

            if results.score == 0.0:
                results.score = "N/A"
            
            container = soup.find("meta", {"itemprop":"ratingCount"})
            if container is not None:
                results.votes = container["content"]
                results.votes = float(results.votes)
            else:
                results.votes = "N/A"
            results.title = soup.find("h1", {"itemprop":"name"})
            results.image = soup.find("img", {"class":"screenshots"})
            results.image = str(results.image)
            results.image = results.image.split('src="')[1].split('?t=')[0]
            results.image = "https://www.anime-planet.com" + results.image

        else:
            results.link = "None"
            results.conv_score = 0.0
            results.score = 0.0
            results.votes = 0.0
            results.title = "None"
            results.image = "None"
    else:
        results.score = 0.0
        results.conv_score = 0.0
        results.votes = 0.0
        results.title = "None"
        results.image = "None"
    return results

#To get data from AniList
def AniList(name):
    results = Data()
    results.link = getLink(name, "AniList", "anilist.co/anime")
    if results.link != "None":
        page = requests.get(results.link)
        soup = BeautifulSoup(page.content, "html5lib")
        element_check = soup.find("script", {"type":"application/ld+json"})
        if element_check is not None:
            container = str(element_check)
            if "ratingValue" in container and "ratingCount" in container:
                results.score = container.split('ratingValue":')[1].split(',')[0]
                results.score = float(results.score)
                results.conv_score = results.score
                results.votes = container.split('ratingCount":')[1].split(',')[0]
                results.votes = float(results.votes)
            else:
                # If "ratingValue" and "ratingCount" not found, then it could be a upcoming anime
                results.score = "N/A"
                results.votes = "N/A"

            results.title = soup.find("title", {"data-vue-meta":"true"})
            results.title = results.title.get_text()
            results.title = results.title.split(" · AniList")[0]
            results.image = soup.find("img", {"class":"cover"})
            results.image = str(results.image)
            results.image = results.image.split('src="')[1].split('"/>')[0]
        else:
            results.link = "None"
            results.score = 0.0
            results.conv_score = 0.0
            results.votes = 0.0
            results.title = "None"
            results.image ="None"
    else:
        results.score = 0.0
        results.conv_score = 0.0
        results.votes = 0.0
        results.title = "None"
        results.image = "None"
    return results