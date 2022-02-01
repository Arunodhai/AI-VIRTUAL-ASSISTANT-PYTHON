import nltk
import numpy as np
#nltk.download('punkt')  #uncomment this when you run the program for the first time.
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, all_words):

    tokenized_sentence=[stem(w) for w in tokenized_sentence]  #this operation is list comprehension.
    bag = np.zeros(len(all_words), dtype=np.float32) #creates an array of length len(all_words) with all values as 0 and the datatype of array is float32.
    for idx,w in enumerate(all_words):  #to get index and word
        if w in tokenized_sentence :
            bag[idx] = 1.0

    return bag
