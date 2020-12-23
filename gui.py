from keras.models import load_model

#Modelimizi loadlıyoruz
model = load_model(r"C:\Users\Cihan\Documents\GitHub\Chatbot\chatbot_model.h5")

import json
import numpy
import random
import yorumlayici
import pickle
import dusukprobability
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

#Jsondaki her sentence
intents = json.loads(open(r"C:\Users\Cihan\Documents\GitHub\Chatbot\veriler.json",encoding="utf8").read())
#Jsondaki her farklı unique kelimeler
words = pickle.load(open(r"C:\Users\Cihan\Documents\GitHub\Chatbot\words.pkl","rb"))
#Her grup ismi
classes = pickle.load(open(r"C:\Users\Cihan\Documents\GitHub\Chatbot\classes.pkl","rb"))

sentencee = None

#Cümleyi kelimelerine ayırır
def clean_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    print(sentence_words)
    sentence_words = [lemmatizer.lemmatize(w.lower()) for w in sentence_words]
    global sentencee
    sentencee = " ".join(sentence_words)
    return sentence_words

#Her cümle için bir bag oluşturur
def bow(sentence, words):
    sentence = clean_sentence(sentence)
    print("sentence = ",sentence)
    bag = [0] * len(words)
    for sent in sentence:
        for w, i in enumerate(words):
            if sent == i:
                bag[w] = 1
    print(bag)
    return (numpy.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words)
    #Alınan bag'in classını öğrenmek için predictler
    res = model.predict(numpy.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # Olasılığı yüksek olandan düşük olana doğru sıralar
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        print(return_list[0]["probability"])
    #Sınıfı ve probability'si ile birlikte döndürür
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    probability = ints[0]["probability"]
    list_of_intents = intents_json['veriler']

    #Eğer alınan response'in doğru olma olasılığı 0.9 dan düşükse düsükprobaility classına girer
    if float(probability) < 0.9:
        print("sentence= ",sentencee)
        yorumlayici.quest = sentencee
        return "Sorduğun sorunun cevabını bilmiyorum,\n\nGoogle'de aratmamı ister misin? (E/H)"
    #Jsondaki bütün intentleri gezip doğru olanı bulduktan sonra cevaplardan restgele bir tanesini seçip cevabı döndürür
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    #Mesaja göre response döndürür
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


            
    
            



