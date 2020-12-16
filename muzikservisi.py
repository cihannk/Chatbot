from multiprocessing import Process
import functs
import playsound

state = []

def playmusic(path):
    print("kako")
    playsound.playsound(path)

def stopmusic():
    state[0].terminate()
    state.clear()

def musicservice(muzikadi):
    mp = Process(target=musicservice2, args=(muzikadi,))
    state.append(mp)
    mp.start()

def musicservice2(muzikadi):
    id = functs.searchid(muzikadi)
    muzikadi = muzikadi.split()
    muzikadi = "".join(muzikadi)
    functs.download_via_id(id, muzikadi)
    path = f"{muzikadi}.mp3"
    playmusic(path)