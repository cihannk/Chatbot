from __future__ import unicode_literals
import youtube_dl
import datetime
import os
import requests
from bs4 import BeautifulSoup
import time
from youtubesearchpython import SearchVideos
import json
import socket

downloaded = 0
internet_connection = None

def is_connected():
    global internet_connection
    try:
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            sock.close
        internet_connection = True
        return True
    except OSError:
        pass
    internet_connection = False
    return False

def mainjsonrequest():
    url = 'https://api.jsonbin.io/b/5fda64203eaf8b71130d61ea'
    req = requests.get(url)
    req = json.loads(req.content)
    print(type(req))

def remove_before_exit():
    files = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) ]
    specified = [s for s in files if s[-3:] == "mp3"]
    for mp3 in specified:
        os.remove(mp3)

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

def exchangeapi():
    try:
        a = requests.get("https://api.exchangeratesapi.io/latest?base=USD")
        if a.status_code == 200:
            print("basarılı")
            a = json.loads(a.content)
            return a["rates"]["TRY"]
    except:
        return None

def api_req(id="qTsaS1Tm-Ic"):
    try:
        a = requests.get(f"https://www.yt-download.org/api/button/mp3/{id}", timeout=(3, 10))
        if a.status_code == 200:
            
            return a.content
    except requests.exceptions.ConnectionError:
        print("connection error")

def scraping(content):
    soup = BeautifulSoup(content, 'html.parser')
    time.sleep(1)
    print(soup.find_all('a', class_='shadow-xl bg-blue-600 text-white hover:text-gray-300 focus:text-gray-300 focus:outline-none rounded-md p-2 border-solid border-2 border-black ml-2 mb-2 w-25'))
    link = soup.find_all('a', class_='shadow-xl bg-blue-600 text-white hover:text-gray-300 focus:text-gray-300 focus:outline-none rounded-md p-2 border-solid border-2 border-black ml-2 mb-2 w-25')[-1]['href']
    time.sleep(1)
    return link

def download(link, mp3_name):
    doc = requests.get(link)
    with open(f'{mp3_name}.mp3', 'wb') as f:
        f.write(doc.content)

def download_via_id(id, name):
    content = api_req(id)
    downlink = scraping(content)
    download(downlink, name)

def searchid(word):
    raw = SearchVideos(word, offset = 1, mode = "json", max_results = 1).result()
    try:
        print(raw)
        link = json.loads(raw)["search_result"][0]["link"]
        link = link[32:]
        return link
    except TypeError:
        return "Internet baglantınız yok."
    

def tr_to_eng(sentence):
    splited = list(sentence)
    tr = ["ş","ı","ö","ğ","ç","ü","Ü","Ç","Ö","İ","Ş"]
    eng = ["s","i","o","g","c","u","U","C","O","I","S"]
    for i in splited:
        if i in tr:
            index= tr.index(i)
            splited[index] = eng[index]
    return "".join(splited)

def catch_int_value(word):
    num = []
    stri = ""
    for l in word:
        try:
            l = int(l)
            num.append(l)
        except ValueError:
            pass
    if len(num) == 0: return 0
    for i in num:
        stri+=str(i)
    return int(stri)

def check_if_exist(name):
    path = f"{name}.mp3"
    files = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) ]
    specified = [s for s in files if s[-3:] == "mp3"]
    for mp3 in specified:
        if mp3 == path:
            return True
    return False

