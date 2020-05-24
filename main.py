# Main program for scraping anime ranking sites
# Author: Ricky Rodriguez

from animescorescraper import MyAnimeList, AnimePlanet, AniList

# A funtion to format output
def TableOutput(website, name, score, votes, link):
    if type(score) == str and type(votes) == str:
        print("%-12s %-15.15s %-8s %-8s" % (website, name, score, votes), link)
    elif type(score) == float and type(votes) == float:
        print("%-12s %-15.15s %-8.2f %-8.0f" % (website, name, score, votes), link)
        
# Main function
while (True):
    anime_search = input("Enter name of anime: ")
    print()
    print("Scraping...")
    print()

    data1 = MyAnimeList(anime_search)
    data2 = AnimePlanet(anime_search)
    data3 = AniList(anime_search)

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
