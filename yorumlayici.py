import muzikservisi
import functs
import sys
import time
import send_info
import processes

def internet_yok():
    functs.is_connected()
    if functs.internet_connection == False:
        return True

def genel_response(msg):

    msgsplited = msg.split()

    if msgsplited[0] == "play":
        functs.is_connected()
        c =[]
        [c.append(x) for x in msgsplited if x != msgsplited[0]]
        b =" ".join(c)

        if functs.internet_connection == True:
             return_msg = muzikservisi.musicservice(b)
             return(return_msg)
             
        else: return "Internet baglantınız yok. Bu servis çalışmayacak."
        
    elif msg == "stop":
        muzikservisi.stopimm()
        return "Müzik durduruldu. "

    elif msg == "quit":
        processes.killmusicprocesses()
        functs.remove_before_exit()
        send_info.send()
        sys.exit()

    else:

        from gui import chatbot_response
        cht = chatbot_response(msg)

        if cht == "saat":
            saat = functs.getTime("now")
            return f"Saat: {saat}"

        elif cht == "gün":
            gun = functs.getTime("day")
            return f"Bugün günlerden {gun}."
        
        elif cht == "yıl":
            yil = functs.getTime("year")
            return f"{yil} yılındayız."
        
        elif cht == "ay":
            ay = functs.getTime("month")
            return f"{ay} ayındayız."

        elif cht == "dolar":
            a = internet_yok()
            print(a)
            if a == True: return "Internet baglantınız yok. Bu servis çalışmayacak."
            else:
                c = functs.catch_int_value(msg)
                dolar_tl = functs.exchangeapi()
                if c == 0:
                    return f"1 USD {dolar_tl} TL"
                else:
                    return f"{c} USD {dolar_tl * c} TL"
                      
        return cht