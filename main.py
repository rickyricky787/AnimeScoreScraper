# Main program for scraping anime ranking sites
# Author: Ricky Rodriguez

from animescorescraper import *

# A funtion to format output
def TableOutput(website, name, score, votes, link):
    print("%-12s %-15.15s %-8s %-8s" % (website, name, score, votes), link)
        
# Main function
if __name__ == "__main__":
    while (True):
        anime_search = input("Enter name of anime: ")
        print()
        print("Scraping...")
        print()

        data1 = MyAnimeListData(MyAnimeListLink(anime_search))
        data2 = AnimePlanetData(AnimePlanetLink(anime_search))
        data3 = AniListData(AniListLink(anime_search))

        TableOutput("Website", "Anime Name", "Score", "Votes", "Link")
        TableOutput("MyAnimeList", data1.title, data1.conv_score, data1.votes, data1.link)
        TableOutput("AnimePlanet", data2.title, data2.conv_score, data2.votes, data2.link)
        TableOutput("Anilist", data3.title, data3.conv_score, data3.votes, data3.link)

        print()
        print("Scores were converted to a scale of 100.")

        print()
        command = input("Enter 'Y' to perform another search. Enter anything else to quit: ")
        print()
        if command == 'Y' or command == 'y':
            continue
        else:
            break