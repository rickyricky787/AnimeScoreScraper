# Anime Ranking Search using BeautifulSoup
# Author: Ricky Rodriguez

import requests
from bs4 import BeautifulSoup
import re

class Data:
    def __int__(self, title = "None", score = 0.0, votes = 0.0, link = "None"):
        self.title = title
        self.score = score
        self.votes = votes
        self.link = link

"""
Def: Finds the link of the anime webpage in a website (MyAnimeList, Anime Planet, Anilist)
Input: User inputed "name", "keyword" and "website" of the webpage we plan on scraping
Output: The link of the anime webpage (if found), "None" (if not found)
"""
def getLink(name, keyword, website):

    # Function will "google" the anime name, followed by the keyword (ex. Pokemon + MyAnimeList).
    # Try to be specific, as it will give you the first link that pops up on google
    # (ex. typing "Hunter X Hunter" would give you results for the 2011 ver., not the 1999 ver.)
    search = name + " " + keyword
    page = requests.get("https://www.google.com/search?q={}&num={}".format(search, 5))
    soup = BeautifulSoup(page.content, "html5lib")
    links = soup.findAll("a")

    
    # In case the first link from the google search is not the website link (ex. a picture),
    # the program will add all the links into an array (only the first 5 links of the frist search page).
    # From then, it will search and select the *first* link found in the array.
    # The link will be stored in the variable THE_LINK
    search_results = []

    for link in links :
        link_href = link.get("href")
        # If not an image "imgurl" or a snippet "?sa=X", add link to array
        if website in link_href and not "imgurl" in link_href and not "?sa=X" in link_href:
            search_results.append(link.get("href").split("?q=")[1].split("&sa=U")[0])

    if len(search_results) != 0:
        THE_LINK = search_results[0]
        return THE_LINK
    else:
        return "None"

def MyAnimeListScrapper(name):
    anime = Data()
    anime.link = getLink(name, "MyAnimeList", "myanimelist.net/anime")
    if anime.link != "None":
        page = requests.get(anime.link)
        soup = BeautifulSoup(page.content, "html5lib") # "soup" means the WHOLE html code
        element_check = soup.select_one("div.fl-l.score") # If element_check is none, then no anime webpage exist
        if element_check is not None:
            container = element_check
            anime.score = container.get_text()
            anime.score = anime.score.strip()
            if anime.score != "N/A":  # An upcoming anime has an "N/A" rating
                anime.score = float(anime.score) * 10
            container = soup.find("span", {"itemprop":"ratingCount"})
            if container is not None:
                anime.votes = container.get_text()
                anime.votes = float(anime.votes)
            else:
                anime.votes = "N/A"
            anime.title = soup.find("span", {"class":"h1-title"})
            anime.title = anime.title.get_text()
        else:
            # If there is no "fl-l.score", then link is incorrect / anime webpage not found
            anime.link = "None"
            anime.score = 0.0
            anime.votes = 0.0
            anime.title = "None"
    else:
        # If no link was returned from getLink(), then anime webpage not found
        # anime.link is already setto "None"
        anime.score = 0.0
        anime.votes = 0.0
        anime.title = "None"
    return anime

def AnimePlanetScrapper(name):
    anime = Data()
    anime.link = getLink(name, "Anime Planet", "anime-planet.com/anime")
    if anime.link != "None":
        page = requests.get(anime.link)
        soup = BeautifulSoup(page.content, "html5lib")
        element_check = soup.select_one("div.avgRating")
        if element_check is not None:
            container = element_check
            anime.score = container.span["style"]
            anime.score = anime.score[7:-1]
            anime.score = float(anime.score)
            if anime.score == 0.0:
                anime.score = "N/A"
            container = soup.find("meta", {"itemprop":"ratingCount"})
            if container is not None:
                anime.votes = container["content"]
                anime.votes = float(anime.votes)
            else:
                anime.votes = "N/A"
            anime.title = soup.find("h1", {"itemprop":"name"})
            anime.title = anime.title.get_text()
        else:
            anime.link = "None"
            anime.score = 0.0
            anime.votes = 0.0
            anime.title = "None"
    else:
        anime.score = 0.0
        anime.votes = 0.0
        anime.title = "None"
    return anime

def AniListScrapper(name):
    anime = Data()
    anime.link = getLink(name, "AniList", "anilist.co/anime")
    if anime.link != "None":
        page = requests.get(anime.link)
        soup = BeautifulSoup(page.content, "html5lib")
        element_check = soup.find("script", {"type":"application/ld+json"})
        if element_check is not None:
            container = str(element_check)
            if "ratingValue" in container and "ratingCount" in container:
                anime.score = container.split('ratingValue":')[1].split(',')[0]
                anime.score = float(anime.score)
                anime.votes = container.split('ratingCount":')[1].split(',')[0]
                anime.votes = float(anime.votes)
            else:
                # If "ratingValue" and "ratingCount" not found, then it could be a upcoming anime
                anime.score = "N/A"
                anime.votes = "N/A"
            anime.title = soup.find("title", {"data-vue-meta":"true"})
            anime.title = anime.title.get_text()
            anime.title = anime.title.split(" · AniList")[0]
        else:
            anime.link = "None"
            anime.score = 0.0
            anime.votes = 0.0
            anime.title = "None"
    else:
        anime.score = 0.0
        anime.votes = 0.0
        anime.title = "None"
    return anime

"""
Def: Function to format the output into a table
Input: Website name, name of the anime, score, votes, and link of the webpage
Output: Anime stats formatted
"""

def TableOutput(website, name, score, votes, link):
    if type(score) == str and type(votes) == str:
        print("%-12s %-15.15s %-8s %-8s" % (website, name, score, votes), link)
    if type(score) == float and type(votes) == float:
        print("%-12s %-15.15s %-8.2f %-8.0f" % (website, name, score, votes), link)
        
####################################################################################
# Main function
while (True):
    anime_search = input("Enter name of anime: ")
    print()
    print("Scraping...")
    print()

    data1 = MyAnimeListScrapper(anime_search)
    data2 = AnimePlanetScrapper(anime_search)
    data3 = AniListScrapper(anime_search)

    TableOutput("Website", "Anime Name", "Score", "Votes", "Link")
    TableOutput("MyAnimeList", data1.title, data1.score, data1.votes, data1.link)
    TableOutput("AnimePlanet", data2.title, data2.score, data2.votes, data2.link)
    TableOutput("Anilist", data3.title, data3.score, data3.votes, data3.link)

    print()
    print("Scores were converted to a scale of 100.")

    print()
    command = input("Enter 'Y' to perform another search. Enter anything else to quit: ")
    print()
    if command == 'Y' or command == 'y':
        continue
    else:
        break
