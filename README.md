# Anime Score Scraper
Scrapes anime scores from MyAnimeList, Anime Planet, and AniList using BeautifulSoup
There are two different versions:
- One that you can run in the terminal (main.py)
- Another one that runs with a GUI using Tkinter (main_gui.py)
- You can also demo it at https://anime-scores.herokuapp.com/

## Purpose
This is just a personal project I did to not only brush up my Python skills, but to also learn how to web scrape using BeautifulSoup. I chose to do an anime score web scraper because I wanted to do a project based on something I enjoy.
I also wanted to learn how to use Tkinter. I had some difficulty layering out the widgets the way I wanted them to be, but as a beginner on Tkinter, I am satisfied with the final product.
- I now added Google Custom Search API to search for queries

## How It Works
Enter the anime you want to know the score of. The program will perform a search on Google for said anime on MyAnimeList, AnimePlanet and AniList, and scrape data. This is done to prevent problems such as a page not finding results for an English name of show if searched directly on site, misspellings, etc. The program will return the title of the anime, score, total number of votes, and a link to its page for each site, all scaled to a score of 100 for easy comparisons.

## How To Run
You must need Python 3 and BeautifulSoup 4 installed in order to run this program.
Extract files to your computer and run **python3 main.py** on terminal.

To use the GUI version, yiu need to have Tkinter, Pillow, and ImageTK installled. Extract files and run **python3 main_gui.py** on terminal.

If you would like to clone and test locally using your own Google API keys:
- Create a .env file with API_KEY = (your Custom Search API key) and SEARCH_ENGINE_ID = (your Search Engine Key)

If you would like to clone and test locally without using Google API keys (not recommended):
- Replace any instance of googleThis() with scrapeGoogle().
- NOTE: Google might set up a captcha after multiple queries, causing the scraper to fail.

(Note: This was tested using Ubuntu 18.04, unsure of how/if it runs on other OS's)

## Preview
![Example](https://github.com/rickyricky787/AnimeScoreScraper/blob/master/example1.png)
![Example](https://github.com/rickyricky787/AnimeScoreScraper/blob/master/example2.png)
![Example](https://github.com/rickyricky787/AnimeScoreScraper/blob/master/example3.png)

(Note: You should check the link if the program scraped the right anime just in case. Some pages might not have a certain version of a title, like an OVA for example, and just scrapes the original)

## Credit
The file **tkHyperlinkManager.py** was created by Fredrik Lundh, modified by me.
(Link: http://effbot.org/zone/tkinter-text-hyperlink.htm)
