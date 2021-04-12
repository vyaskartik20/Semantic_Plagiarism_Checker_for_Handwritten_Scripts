import nltk
from  codes.online_real_plag import websearch
from difflib import SequenceMatcher
import pandas as pd

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(nltk.corpus.stopwords.words('english')) 

def purifyText(string):
    # return string
    words = nltk.word_tokenize(string)
    return (" ".join([word for word in words if word not in stop_words]))

def webVerify(string, results_per_sentence):
    sentences = nltk.sent_tokenize(string)
    matching_sites = []
    for url in websearch.searchBing(query=string, num  = results_per_sentence):
        matching_sites.append(url)
    
    newSentences = sentences
    
    if len(sentences) > 40 :
        newSentences = []
        for i in range(0,(len(sentences)-2),3) :
            try : 
                currSentence = sentences [i] + sentences [i+1] + sentences [i+2]
            
            except :
                try :
                    currSentence = sentences [i] + sentences [i+1]
                except :
                    currSentence = sentences [i]
            
            
            newSentences.append(currSentence)
    
    for sentence in newSentences:
        # print(sentence)
        for url in websearch.searchBing(query = sentence, num = results_per_sentence):
            matching_sites.append(url)

    # print( 'cds           ' + str(len(matching_sites)))
    return (list(set(matching_sites)))






import re, math
from collections import Counter
WORD = re.compile(r'\w+')

#converts given text into a vector
def text_to_vector(text):
     #uses the Regular expression above and gets all words
     words = WORD.findall(text)
     #returns a counter of all the words (count of number of occurences)
     return Counter(words)


def report(text):
      
    matching_sites = webVerify(purifyText(text), 1)
    matches = {}

    # print(len(matching_sites))

    # for i in range(len(matching_sites)):
    #     # score=0
    #     # for sentence in text.split('.'):
    #     #     score=score + similarity(sentence, websearch.extractText(matching_sites[i]))
        
    #     # matches[matching_sites[i]] = score
    #     print(str(matching_sites[i]))        
        
    # matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}

    return(matching_sites)

    # return matches


def returnTable(dictionary):

    # df = pd.DataFrame({'Similarity (%)': dictionary})
    # df = df.fillna(' ').T
    # df = df.transpose()
    # return df
    print('yo')

if __name__ == '__main__':
    report('This is a pure test')
