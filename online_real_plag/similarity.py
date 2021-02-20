import nltk
import websearch
from difflib import SequenceMatcher
import pandas as pd
from rabin import *
from rabin1 import *

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
    # print (str(c1) + '        ' + str(c2) +  '              ' + str(c3) )
    
    if(c1 == 0):
        return -10
    f2 = (c1+c2)/(2*c1)
    f3=(f1*f2)
    print('the plag is :') 
    print(f3)




import re, math
from collections import Counter

WORD = re.compile(r'\w+')

#returns cosine similarity of two vectors
#input: two vectors
#output: integer between 0 and 1.
def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())

     #calculating numerator
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     #calculating denominator
     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     #checking for divide by zero
     if denominator==0:
        return 0.0
     else:
        return float(numerator) / denominator

#converts given text into a vector
def text_to_vector(text):
     #uses the Regular expression above and gets all words
     words = WORD.findall(text)
     #returns a counter of all the words (count of number of occurences)
     return Counter(words)

#returns cosine similarity of two words
#uses: text_to_vector(text) and get_cosine(v1,v2)
def cosineSim(text1,text2):
     vector1 = text_to_vector(text1)
     vector2 = text_to_vector(text2)
     #print vector1,vector2	
     cosine = get_cosine(vector1, vector2)

    #  f1 = len(text1.split())
    #  f2 = len(text2.split())
     
    #  f2 = cosine * 100 * (f1 + f2)
     
    #  if f1 != 0 : 
    #     f1 = f2 / (2*f1)
     
     print('The optimal plag is ' + str(100 * cosine))
     print('')
     return (100 * cosine)









from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 


def cosine2 (X,Y) :
    # Program to measure the similarity between  
    # two sentences using cosine similarity. 
    
    # X = input("Enter first string: ").lower() 
    # Y = input("Enter second string: ").lower() 
    # X ="I love horror movies"
    # Y ="Lights out is a horror movie"
    X=X
    Y=Y
    
    # tokenization 
    X_list = word_tokenize(X)  
    Y_list = word_tokenize(Y) 
    
    # sw contains the list of stopwords 
    sw = stopwords.words('english')  
    l1 =[];l2 =[] 
    
    # remove stop words from the string 
    X_set = {w for w in X_list if not w in sw}  
    Y_set = {w for w in Y_list if not w in sw} 
    
    # form a set containing keywords of both strings  
    rvector = X_set.union(Y_set)  
    for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0
    
    # cosine formula  
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i] 
    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    
    f1 = len(X.split())
    f2 = len(Y.split())
     
    f2 = cosine * 100 * (f1 + f2)
     
    if f1 != 0 : 
        f1 = f2 / (2*f1)
    
    print("similarity: ", (f1)) 












def report(text):
    
    # test=0
    
    # for sentence in text.split('.'):
    #     trial= similarity(sentence, websearch.extractText("http://www.abdulkalam.com/kalam/theme/jsp/guest/myprofile.jsp"))
    #     print(sentence + '             ' + str(trial))
    #     test=test + (trial * len(sentence.split()))
    
    # test=test/(len(text.split()))
    # print('the total plag is      '  + str(test))
    
    
    
    
    
    
    #trial
    
    # text1= purifyText(text).upper()
    # text2= purifyText(websearch.extractText("http://www.abdulkalam.com/kalam/theme/jsp/guest/myprofile.jsp").upper())
    # text3= purifyText(websearch.extractText("https://timesofindia.indiatimes.com/life-style/health-fitness/de-stress/people-with-good-memory-have-these-6-good-habits/photostory/72289863.cms").upper())
    
    # file2=open("assignment_0.txt","w")
    # file2.write(str(text1))
    # file2.close()
    
    # file2=open("assignment_1.txt","w", encoding="utf-8")
    # file2.write((text2))
    # file2.close()
    
    # # with open(fname, "w", encoding="utf-8") as f:
    # # f.write(html)
    
    
    # file2=open("assignment_2.txt","w", encoding="utf-8")
    # file2.write(str(text3))
    # file2.close()

    
    
    # object = OnlinePlag(text1,text2)
    # object.search_main()
    
    
    
    # trial= similarity(text, websearch.extractText("http://www.abdulkalam.com/kalam/theme/jsp/guest/myprofile.jsp"))
    # print(trial)
    
    # trial= cosineSim(text, websearch.extractText("http://www.abdulkalam.com/kalam/theme/jsp/guest/myprofile.jsp"))
    # print(trial)
    
    # print('first')
    # print(text.upper())
    # print(websearch.extractText("https://kidshealth.org/en/teens/brain-nervous-system.html").upper())
    # print('break')
    # print('break')
    # print('break')
    # print('break')
    # print('break')
    # print('break')
    # print('break')
    # print('break')
    # print('break')
    # print('break')
    # print('break')
    # print('break')
    # print('break')
    
    # onject2 = OnlinePlag
    # print('second')
    
    object1 = OnlinePlag(text.upper(), websearch.extractText("http://www.abdulkalam.com/kalam/theme/jsp/guest/myprofile.jsp").upper())
    object1.search_main()
    # search_main(text.upper(), websearch.extractText("https://kidshealth.org/en/teens/brain-nervous-system.html").upper())
    # print(trial)
    
    
    
    # print('third')
    # print(trial)
    # https://kidshealth.org/en/teens/brain-nervous-system.html
    # https://www.cpp.edu/~ftang/courses/CS420/notes/planning.pdf
    
    
    # trial= checker(text, websearch.extractText("http://www.abdulkalam.com/kalam/theme/jsp/guest/myprofile.jsp"))
    # print(trial)
    
    
    # checker = PlagiarismChecker(text1,text2)

    # print('The percentage of plagiarism held by both documents is  {0}%'.format(
    #     checker.get_rate()))
    
    # checker2 = PlagiarismChecker(text1,text3)
    
    
    # print('The percentage of plagiarism held by both documents is  {0}%'.format(
    #     checker2.get_rate()))(text.upper(), websearch.extractText("https://www.cpp.edu/~ftang/courses/CS420/notes/planning.pdf").upper())
    # onject2.search_main()
    
    
    
    
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
    #         trial= cosineSim(sentence, websearch.extractText(matching_sites[i]))
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
    # print ('the actual waala actual plag is :   ')
    # print(score)
    # print('')
    # print('')
    
    # return matches
    
    
    
    
    
    
    #trial
    
    
    

    
    
    # matching_sites = webVerify(purifyText(text), 1)
    # matches = {}

    # # print(len(matching_sites))

    # for i in range(len(matching_sites)):
    #     # score=0
    #     # for sentence in text.split('.'):
    #     #     score=score + similarity(sentence, websearch.extractText(matching_sites[i]))
        
    #     # matches[matching_sites[i]] = score
    #     print(str(matching_sites[i]))
        
   
        # object = OnlinePlag(text.upper(), websearch.extractText(matching_sites[i]).upper())
        # object.search_main()

    #     '''
    #     *******

    #     similarity(text, websearch.extractText(matching_sites[i]))

    #     *******
    #     '''

    #     '''
    #     *******

    #     trial= cosineSim(text, websearch.extractText(matching_sites[i]))
    #     print( matching_sites[i] +   ' :  ' + str(trial) )

    #     *******
    #     '''
        
    #     '''
    #     *******

    #     cosine2(sentence, websearch.extractText(matching_sites[i]))

    #     *******
    #     '''
        
    #     '''
    #     *******

    #     # checker = PlagiarismChecker(purifyText(text), purifyText(websearch.extractText(matching_sites[i])))

    #     # print('The percentage of plagiarism held by both documents is  {0}%'.format(
    #     #     checker.get_rate()))

    #     *******
    #     '''
        
    #     '''
    #     *******
    #     # object = OnlinePlag(text.upper(), websearch.extractText(matching_sites[i]).upper())
    #     # object.search_main()
        
    #     *******
    #     '''
        
        
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
