from __future__ import unicode_literals
import youtube_dl
import datetime
import os
import requests
from bs4 import BeautifulSoup
from playsound import playsound
import multiprocessing
downloaded = 0
state = []

def get_file_names(path=r"C:/Users/Cihan\Documents/GitHub/Chatbot/"):
    names = os.listdir(path)
    return names



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

def save_folder_state():
    state = get_file_names()

def get_diff(recent_state):
    now = get_file_names()
    for i in now:
        if i not in state:
            return i

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
def play(path="myfile.mp3"):
    playsound(path, True)

def playmulti():
    p = multiprocessing.Process(target=play())
    p.start()
    p.terminate()

def stop(p):
    p.stop()
    p.te
playmulti()




