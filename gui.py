from keras.models import load_model

#Modelimizi loadlıyoruz
model = load_model(r"C:\Users\Cihan\Documents\GitHub\Chatbot\chatbot_model.h5")

import json
import numpy
import multiprocessing
import random
import time
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

intents = json.loads(open(r"C:\Users\Cihan\Documents\GitHub\Chatbot\veriler.json",encoding="utf8").read())
words = pickle.load(open(r"C:\Users\Cihan\Documents\GitHub\Chatbot\words.pkl","rb"))
classes = pickle.load(open(r"C:\Users\Cihan\Documents\GitHub\Chatbot\classes.pkl","rb"))

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


            
    
            



