from keras.models import load_model

#Modelimizi loadlıyoruz
model = load_model("chatbot_model.h5")

#Servisler
import ozellikler as svc

import json
import numpy
import multiprocessing
import muzikservisi
import random
import tkinter as tk
import time
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

intents = json.loads(open("veriler.json",encoding="utf8").read())
words = pickle.load(open("words.pkl","rb"))
classes = pickle.load(open("classes.pkl","rb"))

# Girdiğimiz cümleleri parçalara bölmek ve sadeleştirmek için fonksiyon oluşturuyoruz

def clean_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    print(sentence_words)
    sentence_words = [lemmatizer.lemmatize(w.lower()) for w in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence = clean_sentence(sentence)
    print(sentence)
    bag = [0] * len(words)
    for sent in sentence:
        for w, i in enumerate(words):
            if sent == i:
                bag[w] = 1
    print(bag)
    return (numpy.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words)
    #liste halinde predictler
    res = model.predict(numpy.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['veriler']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    print(res, "res", type(res))
    return res

def genel_response(msg):
    msgsplited = msg.split()
    if msgsplited[0] == "play":
        c =[]
        [c.append(x) for x in msgsplited if x != msgsplited[0]]
        b =" ".join(c)
        muzikservisi.musicservice(b)
        return("Muzik servisi basladi, muzik indirilidiğinden çalması biraz gecikebilir. \nMuzigi durdurmak icin stop yazabilirsin. " )

    elif msg == "stop":
        print("stop func icinde")
        muzikservisi.stopmusic()
    else:
        cht = chatbot_response(msg)
        return cht

'''def Bot():
    while True:
        kl = input("Kullanıcı: ")
        if kl.split()[0] == "play":
            kl = kl.split()
            c =[]
            [c.append(x) for x in kl if x != kl[0]]
            b =" ".join(c)
            svc.musicservice(b)
            print("Muzik servisi basladi, muzik indirilidiğinden çalması biraz gecikebilir.")
            print("Muzigi durdurmak icin stop yazabilirsin")
        elif kl == "quit":
            print("Bot: Seninle konuşmak güzeldi...")
            time.sleep(1.5)
            break
        elif kl == "stop":
            print("Müzik durduruluyor...")
        else:
            cb = chatbot_response(kl)
            print("Bot: ",cb) '''


            
    
            



