from multiprocessing import Process
import functs
import playsound
import gui2

def playmusic(path):
    print("kako")
    playsound.playsound(path)

def stopmusic():
    gui2.killmusicprocesses()

def musicservice(muzikadi):
    mp = Process(target=musicservice2, args=(muzikadi,))
    gui2.musicprocesses.append(mp)
    mp.start()
    return "Muzik servisi basladi, muzik indirilidiğinden çalması biraz gecikebilir.\n\nMuzigi durdurmak icin stop yazabilirsin. "

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
