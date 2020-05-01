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



# BFS Algorithm

def spiderBFS(actualURL, depthLevel, numberOfLinks):

    visitedURLS = []
    #queue = deque(['url': seed, 'depth': 1])
    queue = [{'url': actualURL, 'depth': 1}]
    print("Crawling Urls with BFS Algorithm")

    while(len(queue) != 0 and len(visitedURLS) < numberOfLinks):
        node = queue.pop(0)
        if node['url'] not in (obj['url'] for obj in visitedURLS):
            visitedURLS.append(node)
            if(node['depth'] < depthLevel):
                urls = findURL(node)
                if len(urls) != 0:
                    queue = queue + urls
    for j in visitedURLS:
        print(f"\033[91m Url Crawled: {actualURL}{j}")


def spiderDFS(actualURL, depthLevel, numberOfLinks):

    visitedURLS = []
    stack = [{'url': actualURL, 'depth': 1}]
    print("Crawling Urls with DFS Algorithm")

    while(len(stack) != 0 and len(visitedURLS) < numberOfLinks):
        node = stack.pop()
        if node['url'] not in (obj['url'] for obj in visitedURLS):
            visitedURLS.append(node)
            if(node['depth'] < depthLevel):
                urls = findURL(node)
                if len(urls) != 0:
                    stack = stack + urls
    for j in visitedURLS:
        print(f"\033[91m Url Crawled: {actualURL}{j }")



def findURL(node):
    try:
        #time.sleep(1)                                    # be polite and use a delay of at least 1 sec
        html_page = request.urlopen(node['url']).read()   # get and read the file from webpage
        soup = BeautifulSoup(html_page, "html.parser")
        output = []

        # Obtaining urls from raw html page

        for link in soup.findAll('a', href=True):
            if re.search('#', link['href']):        # ignore url that contains '#' (properly treat URLs with #)
                continue
            if re.search(':', link['href']):        # ignore url that contains ':' (avoid administrative link)
                continue
            if link['href'].startswith('/Main_Page') :
                continue
            output.append({'url': urljoin(node['url'], link["href"]), 'depth': node['depth'] + 1})

        return output
    except IOError as err:
        print("No network route to the host".format(err))


def main():

    #Banner
    banner()

    options = ["BFS", "DFS"]

    if len(sys.argv) == 1:
        sys.exit('How to use: python 0xSpider.py https://example.com/ BFS -d 3 -l 50'.format(sys.argv[0]))

    else:
        myURL         = sys.argv[1]
        depthLevel    = int(sys.argv[4])
        numberOfLinks = int(sys.argv[6])

        if sys.argv[2] == options[0]:
            spiderBFS(myURL, depthLevel, numberOfLinks)

        elif sys.argv[2] == options[1]:
            spiderDFS(myURL, depthLevel, numberOfLinks)

if __name__ == '__main__':
    main()
