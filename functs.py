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
    

def tr_to_eng(category, sentence):
    if category == "word":
        tr = ["ş","ı","ö","ğ","ç","ü"]
        eng = ["s","i","o","g","c","u"]
        splited = [x for x in sentence]

        for harf in splited:
            if harf in tr:
                idx = splited.index(harf)
                idx2 = tr.index(harf)
                splited[idx] = eng[idx2]
        return "".join(splited)

    elif category == "month":
        months_eng = "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
        months_tr = "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
        idx = months_eng.index(sentence)
        return months_tr[idx]

    elif category == "day":
        days_eng = "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        days_tr = "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"
        idx = days_eng.index(sentence)
        return days_tr[idx]


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

