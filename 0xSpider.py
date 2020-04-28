from urllib.parse import urljoin
from urllib import request
from collections import deque
from bs4 import BeautifulSoup
import sys
import re


def banner():
    print ("""
\033[0,32m   ___        ____        _     _
  / _ \__  __/ ___| _ __ (_) __| | ___ _ __
 | | | \ \/ /\___ \| '_ \| |/ _` |/ _ \ '__|
 | |_| |>  <  ___) | |_) | | (_| |  __/ |
  \___//_/\_\|____/| .__/|_|\__,_|\___|_|
                   |_|
""")


def spiderBFS(url):

    linkSaved.append(url) # Saved visited urls

    try:
        initialRequest = request.Request(url, headers = headers) # Initial request to the web
        html_page = request.urlopen(initialRequest) # Opening the url
        soup = BeautifulSoup(html_page, 'html.parser') # Downloading the html body of the web
        foundURLs = soup.find_all('a', href=True) # Find all urls in the html, this is a class type

        for i in foundURLs: #Check foundURLs
            flag = 0
            relativeURL = urljoin(url, i["href"]).rstrip('/') #Obtain all URLs from the foundURLs variable

            #queue.apped(url)

            #Check of url is already in the queue
            for u in queue:
                if u == relativeURL:
                    flag = 1
                    break

            # If url not found in queue
            if flag == 0:
                if(linkSaved.count(relativeURL)) == 0: # if linkSaved count how many  relativeURL has saved
                    queue.append(relativeURL)

        current = queue.popleft() # Takes out the current url
        spiderBFS(current)
    except:
        print("I'm not able to find more urls because I've probably been blocked")


def spiderDFS(url):

    linkSaved.append(url) # Saved visited urls

    try:
        initialRequest = request.Request(url, headers = headers) # Initial request to the web
        html_page = request.urlopen(initialRequest) # Opening the url
        soup = BeautifulSoup(html_page, 'html.parser') # Downloading the html body of the web
        foundURLs = soup.find_all('a', href=True) # Find all urls in the html, this is a class type

        for i in foundURLs: #Check foundURLs
            flag = 0
            relativeURL = urljoin(url, i["href"]).rstrip('/') #Obtain all URLs from the foundURLs variable

            #Check of url is already in the queue
            for u in stack:
                if u == relativeURL:
                    flag = 1
                    break

            # If url not found in queue
            if flag == 0:
                if(linkSaved.count(relativeURL)) == 0: # if linkSaved count how many  relativeURL has saved
                    stack.append(relativeURL)

        current = stack.pop() # Takes out the current url
        spiderBFS(current)
    except:
        print("I'm not able to find more urls because I've probably been blocked")

# Main

#Banner
banner()


#Options
options = ["BFS","DFS"]

# Agent that'll visit the given url
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"


if len(sys.argv) == 1:
    print("The arguments are: url algorithm [BFD, DFS]\n")
    print("Example: python Spider.py https://udlap.mx BFS")
else:
    baseUrl = sys.argv[1]
    url = sys.argv[1]
    print("Hi, I'm a Spider")
    print(f"I'm going to scraping this url: {url}\n")

    #Array of visited links, this remains empty at the initial
    linkSaved = []

    if sys.argv[2] == options[0]:

        #This queue will be used
        queue = deque([])
        spiderBFS(url)

    elif sys.argv[2] == options[1]:
        
        #This stack will be used
        stack = []
        spiderDFS(url)

    print(f"I was able to find all these links from: {baseUrl}\n")
    for j in list(set(linkSaved)):
        print(f"\033[91m Url Crawled: {j}")
