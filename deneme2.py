from multiprocessing import Process, Value
import time
import deneme

value = Value("i", 0)

def funct (deger, pname):
    while(deger.value == 1):
        print("deger value 1")
        time.sleep(1)  
    deger.value +=1
    print(deger.value, pname)
    


if __name__ == "__main__":
    pr1 = Process(target=funct, args=(value, "pr1"))
    pr2 = Process(target=funct, args=(value, "pr2"))

    pr1.start()
    time.sleep(3)
    pr2.start()
    pr1.join()
    pr2.join()

    