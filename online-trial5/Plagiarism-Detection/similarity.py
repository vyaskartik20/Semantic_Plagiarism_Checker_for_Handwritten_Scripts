import nltk
import websearch
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
    for sentence in sentences:
        print(sentence)
        for url in websearch.searchBing(query = sentence, num = results_per_sentence):
            matching_sites.append(url)

    print( 'cds           ' + str(len(matching_sites)))
    return (list(set(matching_sites)))


def similarity(str1, str2):
    # str2 = purifyText(str2)
    f1 = (SequenceMatcher(None,str1,str2).ratio())*100
    c1 = len(str1.split())
    c2 = len(str2.split())
    
    c3=((f1/200) * (c1+c2) )
    print (str(c1) + '        ' + str(c2) +  '              ' + str(c3) )
    
    if(c1 == 0):
        return -10
    f2 = (c1+c2)/(2*c1)
    # f2 = (c1+c2)/(2)
    f3=(f1*f2)
    return f3
    

def report(text):
    
    # test=0
    
    # for sentence in text.split('.'):
    #     trial= similarity(sentence, websearch.extractText("http://www.abdulkalam.com/kalam/theme/jsp/guest/myprofile.jsp"))
    #     print(sentence + '             ' + str(trial))
    #     test=test + (trial * len(sentence.split()))
    
    # test=test/(len(text.split()))
    # print('the total plag is      '  + str(test))
    
    
    
    
    
    
    #trial
    
    
    
    
    
    
    
    trial= similarity(text, websearch.extractText("http://www.abdulkalam.com/kalam/theme/jsp/guest/myprofile.jsp"))
    print(trial)
    
    
    
    
    
    
    #trial
    
    
    
    
    
    
    # score=0
    # total=0
        
    # matching_sites = webVerify(purifyText(text), 1)
    # matches = {}

    # sentences = nltk.sent_tokenize(text)

    # for sentence in sentences:
    #     test=-10

    #     print('')
    #     print(sentence)

        
    #     for i in range(len(matching_sites)):
    #         trial= similarity(sentence, websearch.extractText(matching_sites[i]))
    #         print( matching_sites[i] +   ' :  ' + str(trial) )
    #         if(trial>test):
    #             test=trial

    #     # print(' plag of the sentence is  :     ' +  sentence)
    #     # if (len(sentence) != 0) :
    #         # print(str(test) + '          '  +   str(test/len(sentence.split())))  
    #     print('')
    #     print('')
    
    #     if (test != -10):
    #         score=score + (len(sentence.split()) * test)
    #         total = total+len(sentence.split())
    #     # if (test == -10):
    #         # total=total-len(sentence.split())
    #         # score=score-(test * len(sentence.split()) )  

    # if (total != 0) : 
    #     score=(score/total)

    # # matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}

    # print('')
    # print('')
    # print ('the total plag is :   ')
    # print(score)
    # print('')
    # print('')
    
    
    
    
    
    
    #trial
    
    
    

    # return matches
    
    
    # matching_sites = webVerify(purifyText(text), 1)
    # matches = {}

    # print(len(matching_sites))

    # for i in range(len(matching_sites)):
    #     # score=0
    #     # for sentence in text.split('.'):
    #     #     score=score + similarity(sentence, websearch.extractText(matching_sites[i]))
        
    #     # matches[matching_sites[i]] = score

    #     matches[matching_sites[i]] = similarity(text, websearch.extractText(matching_sites[i]))
        
    # matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}

    # return matches


def returnTable(dictionary):

    # df = pd.DataFrame({'Similarity (%)': dictionary})
    # df = df.fillna(' ').T
    # df = df.transpose()
    # return df
    print('yo')

if __name__ == '__main__':
    report('This is a pure test')
