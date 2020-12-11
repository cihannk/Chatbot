# CBot Day 1

import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import tensorflow as tf
import tflearn
import random
import numpy
import json
import pickle

with open("veriler.json", encoding="utf8") as file:
    data = json.load(file)
try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []  # sade olarak bütün pattern kelimeleri
    labels = []  # bütün tagler
    docs_x = []  # bütün patterndeki cümleler
    docs_y = []  # sırasıyla bütün patternedki kelimeler hangi tagla ilişkili

    for veriler in data["veriler"]:
        for pattern in veriler["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(veriler["tag"])

        if veriler["tag"] not in labels:
            labels.append(veriler["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != '?']

    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    print(docs_x)
    print(out_empty)
    for x, doc in enumerate(docs_x):
        print(x, doc)
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]
        print(wrds)
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)


net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:

    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")



