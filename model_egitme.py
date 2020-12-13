import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random

words=[]
classes = []
documents = []
ignore_words = ['?', '!']
# Json dosyasını açtık
with open("veriler.json", encoding="utf8") as d:
    intents = json.load(d)

for intent in intents["veriler"]:
    for pattern in intent["patterns"]:
        #Her patterni tokenize ettik
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        #Tokenize edilmiş patterni tagıyla birlikte documents'e ekledik
        documents.append((w, intent["tag"]))
        # Her farklı tagı (classı) class listesine ekledik
        if intent["tag"] not in classes:
            classes.append(intent["tag"])
        # Lemmatize fonkisyonu ile her sözcükteki tekrarlayan, gereksiz ekleri attık, wordse her kelimeyi ekledik, wordsteki her kelime birbirinden farklı unique kelimeler oldu
        words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]

words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

print (len(documents), "documents", documents)

print (len(classes), "classes", classes)

print (len(words), "unique lemmatized words", words)

pickle.dump(words,open("words.pkl","wb"))
pickle.dump(classes,open("classes.pkl","wb"))

#Eğitilecek datayı oluşturma
training = []
output_zero = [0] * len(classes)
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for  word in pattern_words]
    #Wordsteki her kelimelere bakar eğer pattern_words'te varsa baga 1 ekler öteki durumda 0 ekler, bag tıpkı words dizisi gibidir
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row = list(output_zero)
    #Her bag için karşılık gelen kategori output_row adlı değişkene yazılır (0,0,1,0,0,0) gibi
    output_row[classes.index(doc[1])] = 1
    #Her bag ve output row liste parçası şeklinde training listesine eklenir
    training.append([bag,output_row])

#training listesini karıştıralım
random.shuffle(training)
training = np.array(training)
# Train_X = trainingteki bütün bag'ler, Train_Y = trainingteki bütün class bag'leri
train_x = list(training[:,0])
train_y = list(training[:,1])
#Eğitilecek datamız hazır

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#Modeli kaydediyoruz
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)

print("Model oluşturuldu")

