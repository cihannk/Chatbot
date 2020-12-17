import muzikservisi
import functs
import sys
import gui2

def genel_response(msg):
    msgsplited = msg.split()
    if msgsplited[0] == "play":
        c =[]
        [c.append(x) for x in msgsplited if x != msgsplited[0]]
        b =" ".join(c)
        return_msg = muzikservisi.musicservice(b)
        return(return_msg)

    elif msg == "stop":
        muzikservisi.stopmusic()
        return "Müzik durduruldu. "

    elif msg == "quit":
        gui2.killmusicprocesses()
        functs.remove_before_exit()
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
            c = functs.catch_int_value(msg)
            dolar_tl = functs.exchangeapi()
            if c == 0:
                return f"1 USD {dolar_tl} TL"
            else:
                return f"{c} USD {dolar_tl * c} TL"
        return cht