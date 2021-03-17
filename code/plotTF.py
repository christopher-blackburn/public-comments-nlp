from gensim.utils import simple_preprocess 
from nltk.corpus import stopwords
from collections import Counter
import numpy as np
from nltk.util import ngrams
import matplotlib.pyplot as plt 

stop_words = set(stopwords.words('english'))


def tf(text_data):
    
    '''
    Term frequency computation:
    
    Input: a string  of text
    output: Returns 10 most common terms and frequencies
    '''
    
    # Tokenize and pre-process the data
    filtered_text = [w for w in simple_preprocess(text_data) if not w in stop_words]
    
    # Make bigrams
    bigrams = ngrams(filtered_text,2)
    
    
    # Make trigrams
    trigrams = ngrams(filtered_text,3)
    
    # Top 10 words and term frequency
    def term_freq(x,norm=True):
        bag_of_words = Counter(x)
        if norm == True:
            return np.array(bag_of_words.most_common(10))[:,0],100*np.array(list(map(int,np.array(bag_of_words.most_common(10))[:,1])))/len(bag_of_words)
        else:
            return np.array(bag_of_words.most_common(10))[:,0],100*np.array(list(map(int,np.array(bag_of_words.most_common(10))[:,1])))
    # Return term frequencies
    return term_freq(filtered_text,norm=False), term_freq(bigrams,norm=False), term_freq(trigrams,norm=False)


def plotTF(term_frequency):
    
    unigram, bigram,trigram = term_frequency[0],term_frequency[1],term_frequency[2]
    
    def plotUnigram(unigram):
        plt.barh(unigram[0],unigram[1])
        plt.gca().invert_yaxis()


    def plotBigram(bigram):
        labels = ['-'.join([*bigram_lab]) for bigram_lab in bigram[0]]
        plt.barh(labels,bigram[1])  
        plt.gca().invert_yaxis()


    def plotTrigram(trigram):
        labels = ['-'.join([*trigram_lab]) for trigram_lab in trigram[0]]
        plt.barh(labels,trigram[1])  
        plt.gca().invert_yaxis()



    plt.subplots(figsize=(12,10))
    plotUnigram(unigram),plotBigram(bigram),plotTrigram(trigram)