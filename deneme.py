from multiprocessing import Process, Value
import time
import multiprocessing
ps = []
t = ""
def name (name, sleep):
    global t
    time.sleep(sleep)
    print("adım",int(multiprocessing.current_process().name[-1]))
    t = multiprocessing.current_process().name
    print("ben ",name)


if __name__ == "__main__":
    p1 = Process(target=name, args=("p1",1,))
    p2 = Process(target=name, args=("p2",5,))
    p3 = Process(target=name, args=("p3",10,))

    ps.append(p1)
    ps.append(p2)
    ps.append(p3)
    for i in ps:
        i.start()
    timer = 25    
    while(True):
        if timer == 0: break
        print(t)
        time.sleep(2)
        timer-=2