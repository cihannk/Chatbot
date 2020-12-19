import multiprocessing

musicprocesses = []
isPlaying2 = False

def killspecific(no):
    name = f"Process-{no}"
    print(name)
    for i, pr in enumerate(musicprocesses):
        if pr.name == name:
            print("silmek sitedigim ",pr.name)
            pr.terminate()
            musicprocesses.pop(i)    

def killmusicprocesses():
    try:
        for process in musicprocesses:
            process.terminate()
        musicprocesses.clear()
    except IndexError:
        pass
    except AttributeError:
        pass