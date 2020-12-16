from tkinter import *
import gui as main
import threading
import multiprocessing

global EntryBox
global chat

#Chat penceresi

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

    root = Tk()
    root.title("CBot")
    root.geometry("400x500")
    root.resizable(False, False)

    lbl = Label(root, text ="CBot", fg="white", bg="#bccbeb", font=("verdana", 20, "bold"))

    chat = Text(root, height= 17, width= 37)
    chat.config(font =("Courier", 14), state=DISABLED)
    
    # chat.insert(END, "Bot: " + "Selam, ben CBot. Bana istediğini sorabilirsin\nKapatmak için quit yazabilirsin" + '\n\n')

    scrollbar = Scrollbar(root, command=chat.yview, cursor="heart")
    chat['yscrollcommand'] = scrollbar.set

    #Mesaj gönderme butonu
    buton = Button(root, font=("Verdana",12,"bold"), text= "GONDER", width="8", height="5",bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff', command= send)

    #Mesajların yazılacağı alan
    EntryBox = Text(root, bd=0, bg="white",width="31", height="5", font="Arial")

    scrollbar.place(x=376,y=51, height=360, width=24)
    EntryBox.place(x=5, y=415, height=90, width=280)
    lbl.place(x=0, y=0, width= 400, height=50)
    chat.place(x=0, y=50)
    buton.place(x=300, y=435, height=45)

    root.mainloop()

if __name__ == "__main__":

    mainthread = multiprocessing.Process(target=mainfunc, )
    mainthread.start()