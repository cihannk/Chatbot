from multiprocessing import Process, Value, current_process
import ctypes
import functs
import playsound
import processes
import time
import datetime

isPlaying = Value(ctypes.c_int, 0)
pname = Value(ctypes.c_int, 0)
finish = Value(ctypes.c_int, 0)

def playmusic(path, playing, name):
    zaman = time.time()
    while (playing.value == 1):
        zaman2 = time.time() 
        print(current_process().name, zaman2-zaman, "kadar bekliyor")
        time.sleep(3)
    name.value = int(current_process().name[-1])
    print("ben: ",current_process().name)
    playing.value = 1
    playsound.playsound(path)
    print("tamamlandi")
    playing.value = 0

def stopmusic():
    try:
        processes.musicprocesses[0].terminate()
        processes.musicprocesses.pop(0)
    except IndexError:
        pass

def musicservice(muzikadi):
    print("musicservice= ",isPlaying.value)
    if processes.isPlaying2 == False:
        processes.isPlaying2 = True
        mp = Process(target=musicservice2, args=(muzikadi, isPlaying, pname,))
        processes.musicprocesses.append(mp)
        mp.start()
        print(mp.name)
        return "Muzik servisi basladi, muzik indirilidiğinden çalması biraz gecikebilir.\n\nMuzigi durdurmak icin stop yazabilirsin. "
    else:
        mp = Process(target=musicservice2, args=(muzikadi, isPlaying, pname,))
        processes.musicprocesses.append(mp)
        mp.start()
        print(mp.name)
        return "Şuan şarkı yürütüldüğünden istediğiniz şarkı sıraya eklendi."

def musicservice2(muzikadi, playing, prname):
    muzikadi = muzikadi.split()
    muzikadi = "".join(muzikadi)

    if functs.check_if_exist(muzikadi):
        path = f"{muzikadi}.mp3"
        playmusic(path, playing, prname)
        return 0
        
    id = functs.searchid(muzikadi)
    try:
        functs.download_via_id(id, muzikadi)
    except:
        return muzikadi
    path = f"{muzikadi}.mp3"
    playmusic(path, playing, prname)
    return 0
    
def network_error(id):
    processes.killmusicprocesses()
    return id

def startnext(playing):
    playing.value = 0

def stopimm():
    print("silinmek ist:" , pname.value)
    proc = Process(target=startnext, args=(isPlaying,))
    try:
        processes.killspecific(pname.value)
    except IndexError:
        pass
    proc.start()
    proc.join()

