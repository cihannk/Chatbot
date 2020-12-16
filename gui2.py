from tkinter import *
import gui as main
import threading
import multiprocessing
import muzikservisi

global EntryBox
global chat

mainprocesses = []
musicprocesses = []
flag = True

def killmusicprocesses():
    for process in musicprocesses:
        process.terminate()
    musicprocesses.clear()

#Chat penceresi

def baslangic_mesaji():
    res = "Merhaba, Ben CBot. Bana istediğini sorabilirsin.\nProgramdan çıkmak için {quit} yazabilirsin."
    chat.config(state=NORMAL)
    chat.insert(END, "Bot: " + res + '\n\n')
    chat.config(foreground="#442265", font=("Verdana", 12 ))
    chat.config(state=DISABLED)
    chat.yview(END)

def send():
    
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        chat.config(state=NORMAL)
        chat.insert(END, "Sen: " + msg + '\n\n')
        chat.config(foreground="#442265", font=("Verdana", 12 ))

        res = main.genel_response(msg)
        chat.insert(END, "Bot: " + res + '\n\n')

        chat.config(state=DISABLED)
        chat.yview(END)

def mainfunc():
    global EntryBox
    global chat
    global flag

    root = Tk()
    root.title("CBot")
    root.geometry("400x500")
    root.resizable(False, False)

    lbl = Label(root, text ="CBot", fg="white", bg="#bccbeb", font=("verdana", 20, "bold"))

    chat = Text(root, height= 17, width= 37)
    chat.config(font =("Courier", 14), state=DISABLED)

    scrollbar = Scrollbar(root, command=chat.yview, cursor="heart")
    chat['yscrollcommand'] = scrollbar.set

    #Mesaj gönderme butonu
    buton = Button(root, font=("Verdana",12,"bold"), text= "GONDER", width="8", height="5",bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff', command= send)

    #Mesajların yazılacağı alan
    EntryBox = Text(root, bd=0, bg="white",width="31", height="5", font="Arial")

    scrollbar.place(x=376,y=60, height=310, width=24)
    EntryBox.place(x=10, y=385, height=90, width=280)
    lbl.place(x=0, y=0, width= 400, height=50)
    chat.place(x=0, y=50)
    buton.place(x=300, y=405, height=55)

    if flag == True:
        baslangic_mesaji()
        flag == False

    root.mainloop()

if __name__ == "__main__":

    mainthread = multiprocessing.Process(target=mainfunc, )
    mainprocesses.append(mainthread)
    mainthread.start()