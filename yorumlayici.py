import muzikservisi
import functs
import sys
import time
import send_info
import processes
import dusukprobability

bilgigonder = True
quest = None
yesno = 0 #0-Boşta, 1-Onayladı, 2-Onaylamadı
yesnoneccesary = False
category = None


def yes_or_no(msg):
    global yesno
    expected=["e","E","h","H"]
    if msg in expected and (msg == expected[0] or msg == expected[1]):
        yesno = 1
    elif msg in expected and (msg == expected[2] or msg == expected[3]):
        yesno = 2
    else:
        return "E/H şeklinde cevap verebilirsin."
        
def returnspecified():
    global yesno
    global category
    global yesnoneccesary
    if category == "google" and yesno == 1:
        try:
            category = None
            yesno = 0
            yesnoneccesary = False
            link = dusukprobability.quickanswer(quest)
            dusukprobability.first_result = link
            return f"Boyle bir link buldum\n\n{link}\n\n[aç] yazarsan senin için açabilirim."
        except:
            return "Internet baglantın olmadığından google servisi kullanılamıyor."    
    else:
        category = None
        yesno = 0
        yesnoneccesary = False
        return "İptal edildi"

def genel_response(msg):
    global yesnoneccesary
    global category
    global bilgigonder

    msgsplited = msg.split()
    if yesnoneccesary == True:
        if functs.is_connected() != True:
            yesnoneccesary = False
            return "Internet baglantın olmadığından google servisi kullanılamıyor."
        word = yes_or_no(msg)
        if word != None:
            return word
        x = returnspecified()
        if x!= None:
            return x
    if msgsplited[0] == "play":
        is_connected= functs.is_connected()
        c =[]
        #Cümleden play kelimesini çıkarır -> Cümleye dönüştürür
        [c.append(x) for x in msgsplited if x != msgsplited[0]]
        b =" ".join(c)
        birlesik = b.split()
        birlesik = "".join(birlesik)
        b = b.lower()
        b = functs.tr_to_eng("word", b)

        if is_connected == True:
             return_msg = muzikservisi.musicservice(b)
             if return_msg == 1:
                 return "1"
             return(return_msg)
        else:
            if functs.check_if_exist(birlesik):
                return_msg = muzikservisi.musicservice(b)
                return return_msg
            else:
                return "Internet baglantınız yok. Bu servis çalışmayacak."
        
    elif msg == "stop":
        muzikservisi.stopimm()
        return "Müzik durduruldu. "

    elif msg == "bilgigonderme":
        bilgigonder = False
        return "Değişiklikleriniz onaylandı."

    elif msg == "aç":
        dusukprobability.open_link()
        return "açılıyor..."

    elif msg == "quit":
        processes.killmusicprocesses()
        functs.remove_before_exit()
        if bilgigonder:
            send_info.send()
        sys.exit()

    else:
        #Eğer bütün ana komutlar harici bir mesaj yazılmışsa import eder
        #Yapay zekanın cevabına göre başka servisler tetiklenebilir
        from gui import chatbot_response
        cht = chatbot_response(msg)

        if cht == "saat":
            saat = functs.getTime("now")
            return f"Saat: {saat}"

        elif cht == "gün":
            gun = functs.getTime("day")
            gun= functs.tr_to_eng("day", gun)
            return f"Bugün günlerden {gun}."
        
        elif cht == "yıl":
            yil = functs.getTime("year")
            return f"{yil} yılındayız."
        
        elif cht == "ay":
            ay = functs.getTime("month")
            ay= functs.tr_to_eng("month", ay)
            return f"{ay} ayındayız."

        elif cht == "dolar":
            a = functs.is_connected()
            print(a)
            if a == False: return "Internet baglantınız yok. Bu servis çalışmayacak."
            c = functs.catch_int_value(msg)
            dolar_tl = functs.exchangeapi()
            if c == 0:
                return f"1 USD {dolar_tl} TL"
            else:
                return f"{c} USD {dolar_tl * c} TL"
        elif cht == "Sorduğun sorunun cevabını bilmiyorum,\n\nGoogle'de aratmamı ister misin? (E/H)":
            yesnoneccesary = True
            category = "google"
                      
        return cht