import tkinter
import multiprocessing
import yorumlayici
import send_info
import datetime
import functs
import send_info
import sys
import processes

global EntryBox
global chat

flag = True
internet_connection = None

#Kapanırken çalışan fonksiyon
def on_closing():
    processes.killmusicprocesses()
    functs.remove_before_exit()
    send_info.send()
    sys.exit()

#Chat penceresi

def baslangic_mesaji(msg=""):
    res = f"{msg}Merhaba, Ben CBot. Bana istediğini sorabilirsin.\n\nProgramdan çıkmak için quit yazabilirsin. \n\nKomutları öğrenmek için komutlar yazabilirisin"
    chat.config(state=tkinter.NORMAL)
    chat.insert(tkinter.END, "Bot: " + res + '\n\n')
    chat.config(foreground="#442265", font=("Verdana", 12 ))
    chat.config(state=tkinter.DISABLED)
    chat.yview(tkinter.END)

#Butona tıklandıktan sonra tetiklenecek fonksiyon
def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    send_info.commands.append(msg)
    send_info.times.append(datetime.datetime.now().strftime("%d %b %Y %H:%M:%S"))
    EntryBox.delete("0.0",tkinter.END)
    if msg != '':
        chat.config(state=tkinter.NORMAL)
        chat.insert(tkinter.END, "Sen: " + msg + '\n\n')
        chat.config(foreground="#442265", font=("Verdana", 12 ))
        #Responseyi almak için önce yorumlayıcıya gider
        res = yorumlayici.genel_response(msg)
        chat.insert(tkinter.END, "Bot: " + res + '\n\n')
        chat.config(state=tkinter.DISABLED)
        chat.yview(tkinter.END)     

#Projenin main bölümü
if __name__ == "__main__":

    #Pencereyi oluşturuyorum
    multiprocessing.freeze_support()
    root = tkinter.Tk()
    root.title("CBot")
    root.geometry("400x500")
    root.resizable(False, False)

    lbl = tkinter.Label(root, text ="CBot", fg="white", bg="#bccbeb", font=("verdana", 20, "bold"))

    #Chat alanı
    chat = tkinter.Text(root, height= 17, width= 37)
    chat.config(font =("Courier", 14), state=tkinter.DISABLED)

    scrollbar = tkinter.Scrollbar(root, command=chat.yview, cursor="heart")
    chat['yscrollcommand'] = scrollbar.set

    #Mesaj gönderme butonu
    buton = tkinter.Button(root, font=("Verdana",12,"bold"), text= "GONDER", width="8", height="5",bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff', command= send)

    #Mesajların yazılacağı alan
    EntryBox = tkinter.Text(root, bd=0, bg="white",width="31", height="5", font="Arial")

    scrollbar.place(x=376,y=60, height=310, width=24)
    EntryBox.place(x=10, y=385, height=90, width=280)
    lbl.place(x=0, y=0, width= 400, height=50)
    chat.place(x=0, y=50)
    buton.place(x=300, y=405, height=55)

    #Programı ilk çalıştırdığımızda başlangıç mesajı ve internet bağlantı kontrolü yapılan yer
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
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

