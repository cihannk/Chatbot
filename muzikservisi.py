from multiprocessing import Process, Value
import functs
import playsound
import gui2
import time
import datetime

def playmusic(path):
    while (gui2.isPlaying): 
        print(datetime.datetime.now())
        time.sleep(1)
    gui2.isPlaying = True
    playsound.playsound(path)
    print("tamamlandi")
    stopmusic()

def stopmusic():
    gui2.isPlaying = False
    try:
        gui2.musicprocesses[0].terminate()
        gui2.musicprocesses.pop(0)
    except IndexError:
        pass

def musicservice(muzikadi):
    print(gui2.isPlaying)
    if gui2.isPlaying2 == False:
        gui2.isPlaying2 = True
        mp = Process(target=musicservice2, args=(muzikadi,))
        gui2.musicprocesses.append(mp)
        mp.start()
        return "Muzik servisi basladi, muzik indirilidiğinden çalması biraz gecikebilir.\n\nMuzigi durdurmak icin stop yazabilirsin. "
    else:
        mp = Process(target=musicservice2, args=(muzikadi,))
        gui2.musicprocesses.append(mp)
        mp.start()
        return "Şuan şarkı yürütüldüğünden istediğiniz şarkı sıraya eklendi."

def musicservice2(muzikadi):
    id = functs.searchid(muzikadi)
    if id[0] == "I": network_error(id)
    muzikadi = muzikadi.split()
    muzikadi = "".join(muzikadi)
    functs.download_via_id(id, muzikadi)
    path = f"{muzikadi}.mp3"
    playmusic(path)
    

def network_error(id):
    gui2.killmusicprocesses()
    return id
