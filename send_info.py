import smtplib, ssl
import getpass
import json

sender_email = "cbot.nightblack@gmail.com"
to = "cihanov8@gmail.com"
password = "rgstdtfacfgfympm"

commands=[]
times=[]

# Create a secure SSL context
context = ssl.create_default_context()


def send_mail(content):
    FROM = sender_email
    TO = to
    SUBJECT = "CBot"
    TEXT = content
    pwd = password

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(FROM, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")

def user():
    return getpass.getuser()

def createjson():
    data = []
    for i in range(len(commands)):
        data.append([commands[i], times[i]])
    a = dict()
    a["hostname"] = user()
    a["messages"] = data
    a = json.dumps(a)
    print(a,type(a))
    return a

def send():
    json = createjson()
    send_mail(json)
