import os

dirs = os.listdir()
dir_path = os.path.dirname(os.path.realpath(__file__))
srcpath = dir_path + r"\\src\\"
modelpath = srcpath+ "chatbot_model.h5"
classespath = srcpath + "classes.pkl"
jsonpath = srcpath + "veriler.json"
wordspath = srcpath + "words.pkl"

print(wordspath)