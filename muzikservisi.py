from multiprocessing import Process
import ozellikler
import playsound
import ozellikler

state = []

def playmusic(path):
    print("kako")
    playsound.playsound(path)

def stopmusic():
    state[0].terminate()


def musicservice(muzikadi):
    mp = Process(target=musicservice2, args=(muzikadi,))
    state.append(mp)
    mp.start()

def musicservice2(muzikadi):
    id = ozellikler.searchid(muzikadi)
    muzikadi = muzikadi.split()
    muzikadi = "".join(muzikadi)
    ozellikler.download_via_id(id, muzikadi)
    path = f"{muzikadi}.mp3"
    playmusic(path)