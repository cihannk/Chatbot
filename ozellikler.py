from __future__ import unicode_literals
import youtube_dl
import datetime
import os
import requests
from bs4 import BeautifulSoup
from playsound import playsound
from threading import Thread
import time
import sys
from youtubesearchpython import SearchVideos
import json

downloaded = 0
state = []
jobs= []



def getTime(type):
    timenow = datetime.datetime.now()
    if type == "now":
        current_time = timenow.strftime("%H:%M:%S")
        return current_time
    elif type == "month":
        return timenow.strftime("%B")
    elif type == "year":
        return timenow.strftime("%Y")
    elif type == "day":
        return timenow.strftime("%A")


def api_req(id="qTsaS1Tm-Ic"):
    a = requests.get(f"https://www.yt-download.org/api/button/mp3/{id}")
    if a.status_code == 200:
        return a.content

def scraping(content):
    soup = BeautifulSoup(content, 'html.parser')
    link = soup.find_all('a', class_='shadow-xl bg-blue-600 text-white hover:text-gray-300 focus:text-gray-300 focus:outline-none rounded-md p-2 border-solid border-2 border-black ml-2 mb-2 w-25')[-1]['href']
    return link

def download(link, mp3_name):
    print("link: ",link)
    doc = requests.get(link)
    with open(f'{mp3_name}.mp3', 'wb') as f:
        f.write(doc.content)

def download_via_id(id, name):
    content = api_req(id)
    downlink = scraping(content)
    download(downlink, name)

def playmusic(path):
    print("a")
    playsound(path, True)

def threading(path):
    return Thread(target=playmusic, args=(path,), name="t")

def searchid(word):
    search = SearchVideos(word, offset = 1, mode = "json", max_results = 1)
    raw = search.result()
    link = json.loads(raw)["search_result"][0]["link"]
    print(link)
    link = link[32:]
    return link
    

'''
a = threading("muzik.mp3")
a.daemon = True
a.start()
print("hop")
time.sleep(6)
a._stop '''

searchid("Enes batur yutup")


