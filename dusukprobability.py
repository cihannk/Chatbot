definedcategories = []
full_sentence_arry= []
first_result= None
sentence = None
googlekeywords = ["nedir", "kaçtır", "ne", "nasıl", "ne zaman", "kim", "kimdir"]

import googlesearch
import gsearch
import webbrowser

def open_link():
    try:
        webbrowser.open_new(first_result)
    except:
        pass

def put(full_sentence, definedcategory):
    global definedcategories
    global full_sentence_arry
    global sentence
    global first_result
    definedcategories = definedcategory
    full_sentence_arry = full_sentence
    sentence = " ".join(full_sentence_arry)
    responses  = googleservice()
    first_result = responses[1]
    print(responses)
    return f"Sorduğun sorunun cevabını bilmiyorum,\n\nGoogle'de aratmamı ister misin? (E/H)" #  böyle bir link buldum:\n\n{first_result}\n\n[aç] yazarsan senin için açabilirim."

def quickanswer(question):
    response = gsearch.search(question, num_results=10, lang="tr")
    return response[1]

def definewhichservice():
    for word in full_sentence_arry:
        if word in googlekeywords:
            pass

def googleservice():
    response = gsearch.search(sentence, num_results=10, lang="tr")
    return response
    
