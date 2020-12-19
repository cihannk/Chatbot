from tkinter import *
import multiprocessing
import muzikservisi
import yorumlayici
import send_info
import datetime
import functs

global EntryBox
global chat

flag = True
internet_connection = None

#Chat penceresi

def baslangic_mesaji(msg=""):
    res = f"{msg}Merhaba, Ben CBot. Bana istediğini sorabilirsin.\n\nProgramdan çıkmak için quit yazabilirsin. \n\nKomutları öğrenmek için komutlar yazabilirisin"
    chat.config(state=NORMAL)
    chat.insert(END, "Bot: " + res + '\n\n')
    chat.config(foreground="#442265", font=("Verdana", 12 ))
    chat.config(state=DISABLED)
    chat.yview(END)

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    send_info.commands.append(msg)
    send_info.times.append(datetime.datetime.now().strftime("%d %b %Y %H:%M:%S"))
    EntryBox.delete("0.0",END)
    if msg != '':
        chat.config(state=NORMAL)
        chat.insert(END, "Sen: " + msg + '\n\n')
        chat.config(foreground="#442265", font=("Verdana", 12 ))

        res = yorumlayici.genel_response(msg)
        chat.insert(END, "Bot: " + res + '\n\n')

        chat.config(state=DISABLED)
        chat.yview(END)

if __name__ == "__main__":
    multiprocessing.freeze_support()
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
        isconnected = functs.is_connected()
        print(isconnected)
        if isconnected == False: 
            internet_connection = False
            baslangic_mesaji("Internet baglantınız olmadıgından bazı servisler çalışmayacaktır.\n\n")
        else:
            internet_connection = True
            baslangic_mesaji()
        flag == False

    root.mainloop()

