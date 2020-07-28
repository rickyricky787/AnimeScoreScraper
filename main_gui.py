# Anime Score Scraper with GUI
# Author: Ricky Rodriguez

import tkinter as tk
import webbrowser
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO

import tkHyperlinkManager
from animescorescraper import MyAnimeList, AnimePlanet, AniList
 

# Create an instance of the Tk class
win = tk.Tk()

#Set window size
win.geometry("215x315")
win.resizable(False, False)
win.config(bg = "cornflowerblue")

# Adding a title to the GUI
win.title("Anime Score Scraper")

# Create left and right frames
left_side = tk.Frame(win, width = 225, height = 325, bg = 'cornflowerblue')
left_side.grid(row = 0, column = 0, padx = 10, pady = 5)

right_side = tk.Frame(win, width=225, height=325, bg = 'cornflowerblue')
right_side.grid(row = 0, column = 1, padx = 10, pady = 5)

tool_bar = tk.Frame(left_side, width = 180, height = 185, bg = 'cornflowerblue')
tool_bar.grid(row = 2, column = 0, padx = 5, pady = 5)

# Example labels that serve as placeholders for other widgets 
intro = tk.Label(tool_bar, text = "Enter anime name: ", bg = 'cornflowerblue')
intro.grid(row = 1, column = 0, padx = 5, pady = 3, ipadx = 10)

#Adding a blank fill
name = tk.StringVar()
name_entered = tk.Entry(tool_bar, width = 20, textvariable = name)
name_entered.grid(row = 2, column = 0, padx = 8, pady = 10)

#Adding stuff that will pop up after click
search_label = tk.Label(tool_bar)
images = []
panel = tk.Label(right_side)

#Function that will get image from link to tkinker
def add_image(image_link):
    response = requests.get(image_link)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = ImageTk.PhotoImage(img.resize((225,325)))
    response.close()
    return img

# Command when you click something
def click_me(event = "None"):
    win.geometry("800x400")
    

    search_label.configure(text="Search results for: " + name.get(), bg = 'cornflowerblue')
    search_label.grid(row = 4, column = 0, padx = 8, pady = 10)

    right_side.configure(bg='white')

    # Functions to scrape data
    anime_search = name.get()
    myanime_data = MyAnimeList(anime_search)
    aniplanet_data = AnimePlanet(anime_search)
    anilist_data = AniList(anime_search)

    # Creating textbox
    text = tk.Text(tool_bar, width = 50, height = 5)
    text.grid(row = 5, column = 0, padx = 8, pady = 20)

    # Quirky formating
    myanime_data.title = myanime_data.title[:15]
    while (len(myanime_data.title) < 15):
        myanime_data.title += " "

    aniplanet_data.title = aniplanet_data.title[:15]
    while (len(aniplanet_data.title) < 15):
        aniplanet_data.title += " "

    anilist_data.title = anilist_data.title[:15]
    while (len(anilist_data.title) < 15):
        anilist_data.title += " "

    link1 = lambda : webbrowser.open(myanime_data.link)
    link2 = lambda : webbrowser.open(aniplanet_data.link)
    link3 = lambda : webbrowser.open(anilist_data.link)
    hyperlink = tkHyperlinkManager.HyperlinkManager(text)

    #

    # Inserting into textbox
    text.insert(tk.END, "Website" + "       " + "Title" + "             " + "Score" + "   " + "Votes\n")
    text.insert(tk.END, "--------------------------------------------------\n")
    text.insert(tk.END, "MyAnimeList", hyperlink.add(link1))
    text.insert(tk.END, "   " + myanime_data.title + "   " + myanime_data.conv_score + "   " + myanime_data.votes + "\n")
    text.insert(tk.END, "AnimePlanet", hyperlink.add(link2))
    text.insert(tk.END, "   " + aniplanet_data.title + "   " + aniplanet_data.conv_score + "   " + aniplanet_data.votes + "\n")
    text.insert(tk.END, "AniList", hyperlink.add(link3))
    text.insert(tk.END, "       " + anilist_data.title + "   " + anilist_data.conv_score + "   " + anilist_data.votes + "\n")
    text.configure(state='disabled')

    # Only add image if it is found
    img_url = anilist_data.image
    if (img_url != "None"):
        img = add_image(img_url)
        panel.configure(image = img, bg = 'cornflowerblue')
        panel.grid(row = 0, column = 0, padx = 5, pady = 5)
        images.append(img)

    tk.Label(tool_bar, text = "Scores are scaaled to a score of 100", bg = 'cornflowerblue').grid(row = 6, column = 0, padx=5, ipadx = 10)
    tk.Label(tool_bar, text = "Click link to open to website", bg ='cornflowerblue').grid(row = 7, column = 0, padx = 5, ipadx = 10)
    tk.Label(tool_bar, text = "Check spelling / be more accurate if different title was found", bg = 'cornflowerblue').grid(row = 8, column = 0, padx = 5, ipadx = 10)
    tk.Label(right_side, text = "Image from AniList", bg = 'white').grid(row = 1, column = 0, padx=5, ipadx = 10)

#Adding a button
tk.Button(tool_bar, text = "Search", command = click_me).grid(row = 3, column = 0)
win.bind("<Return>", click_me)

#Start GUI
win.mainloop()
