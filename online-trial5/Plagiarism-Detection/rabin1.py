import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
import numpy as np
from os.path import dirname, join
import re
import math


class PlagiarismChecker:
    def __init__(self, file_a, file_b):
        self.file_a = file_a
        self.file_b = file_b
        self.hash_table = {"a": [], "b": []}
        self.k_gram = 3
        content_a = (self.file_a)
        content_b = (self.file_b)
        self.calculate_hash(content_a, "a")
        self.calculate_hash(content_b, "b")

    # calaculate hash value of the file content
    # and add it to the document type hash table
    def calculate_hash(self, content, doc_type):
        text = self.prepare_content(content)
        text = "".join(text)
        # print(text)

        text = rolling_hash(text, self.k_gram)
        for _ in range(len(content) - self.k_gram + 1):
            self.hash_table[doc_type].append(text.hash)
            if text.next_window() == False:
                break
        # print(self.hash_table)

    def get_rate(self):
        return self.calaculate_plagiarism_rate(self.hash_table)

    # calculate the plagiarism rate using the plagiarism rate formula
    def calaculate_plagiarism_rate(self, hash_table):
        th_a = len(hash_table["a"])
        th_b = len(hash_table["b"])
        a = hash_table["a"]
        b = hash_table["b"]
        sh = len(np.intersect1d(a, b))
        # print(sh, a, b)
        print(sh, th_a, th_b)

        # Formular for plagiarism rate
        # P = (2 * SH / THA * THB ) 100%
        p = (float( sh)/(th_a)) * 100
        return p

    # get content from file
    def get_file_content(self, filename):
        file = open(filename, 'r+', encoding="utf-8")
        return file.read()

    # Prepare content by removing stopwords, steemming and tokenizing
    def prepare_content(self, content):
        # STOP WORDS
        stop_words = set(stopwords.words('english'))
        # TOKENIZE
        word_tokens = word_tokenize(content)

        filtered_content = []
        # STEMMING
        porter = PorterStemmer()
        for w in word_tokens:
            if w not in stop_words:
                w = w.lower()
                word = porter.stem(w)
                filtered_content.append(word)

        return filtered_content

print('kartik')

# current_dir = dirname(__file__)
# checker = PlagiarismChecker(
#     join(current_dir, "../docs/document_a.txt"),
#     join(current_dir, "../docs/document_b.txt")
# )

# print('The percentage of plagiarism held by both documents is  {0}%'.format(
#     checker.get_rate()))




class rolling_hash:
    def __init__(self, text, patternSize):
        self.text = text
        self.patternSize = patternSize
        self.base = 26
        self.window_start = 0
        self.window_end = 0
        self.mod = 5807
        self.primes = (23,209,3007,40007,500007,6000007,70000007,800007,97,100007,10017,127,10000037,1407,10057)
        self.hash = self.get_hash(text, patternSize)

    def get_hash(self, text, patternSize):
        hash_value = 0
        for i in range(0, patternSize):
            # temp = (ord(self.text[i]) - 96)*(self.base*(patternSize - i - 1))% self.mod
            # temp=(temp) % self.mod
            # hash_value = (hash_value + (temp) )% self.mod
            hash_value = (
                hash_value  * math.pow(77,i) + (self.primes[i]*  (ord(self.text[i]) - 96)*(self.base**(patternSize - i - 1)))) % self.mod
            # hash_value = (
                # hash_value + math.pow(7,i) * self.primes[i]* (ord(self.text[i]) - 96)*(self.base**(patternSize - i - 1))) % self.mod

        self.window_start = 0
        self.window_end = patternSize

        return hash_value
    
    # def rolling_hash(self,prev,next,present_hash):
    #     next_hash=present_hash
    #     for i,prime in  enumerate(prime_nos):
    #         next_hash[i]=next_hash[i]-prev
    #         next_hash[i]=next_hash[i]/prime
    #         next_hash[i]=next_hash[i]+next*math.pow(prime,2)
    #     return next_hash

    def next_window(self):
        if self.window_end <= len(self.text) - 1:
            self.hash -= (ord(self.text[self.window_start]) -
                          96)*self.base**(self.patternSize-1)

            self.hash *= self.base
            self.hash += ord(self.text[self.window_end]) - 96
            # print(  ord(self.text[self.window_end])- 96)
            self.hash %= self.mod
            self.window_start += 1
            self.window_end += 1
            return True
        return False

    def current_window_text(self):
        return self.text[self.window_start:self.window_end]


def checker(text, pattern):
    if text == "" or pattern == "":
        return None
    if len(pattern) > len(pattern):
        return None

    text_rolling = rolling_hash(text.lower(), len(pattern))
    pattern_rolling = rolling_hash(pattern.lower(), len(pattern))

    for _ in range(len(text)-len(pattern)+1):
        # print(pattern_rolling.hash, text_rolling.hash)
        if text_rolling.hash == pattern_rolling.hash:
            return "Found"
        text_rolling.next_window()
    return "Not Found"


# if __name__ == "__main__":
    # print(checker("ABDCCEAGmsslslsosspps", "agkalallaa"))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 
 
 
# from bloom_filter import *
# from aho import *
# from collections import deque
# import ahocorasick as ahc
# import math
# import os
# from os import path
# global prime_nos,phrases,word_code,input_phrases,input_phrases_idx
# prime_nos=(113,117,119,123,129,131,137)
# phrases=[]
# word_code=[]
# input_phrases=[]
# input_phrases_idx=[]

# class OnlinePlag : 
    
#     def __init__(self,test_text, source_text):
#         self.test_text = test_text
#         self.source_text=source_text
    
    
#     def detector(self,patt_file,input_file):
#         f=bloom_filter(10000007)
#         input_code=deque()

#         phrases,word_code=self.convertPhrases(patt_file)

#         self.phraseMapping(word_code,f)

#         input_phrases,input_phrases_idx=self.scanInput(input_file,input_code,f)

#         patterns=self.filter_word(phrases,word_code,f)

#         input_phrases,input_phrases_idx=self.exactMatching(input_phrases,patterns)

#         commonwords=self.calc_plag(input_phrases,input_phrases_idx)

#         self.percentage_calc(commonwords,patt_file,input_file)


#     def convertPhrases(self,patt_file):
#         ascii_code=0
#         word=''
#         appended=True
#         window=deque()
#         for c in patt_file:
#             if 'A'<=c<'Z':  
#                 ascii_code=ascii_code+ord(c)-65
#                 word=word+c
#                 appended=False
#             else: 
#                 if appended is False:
#                     word_code.append(ascii_code)
#                     window.append(word)
#                     if len(window)==3:
#                         k=' '.join(list(window))
#                         phrases.append(k)
#                         window.popleft()
#                     ascii_code=0
#                     word=''
#                     appended=True
#         # print(phrases)
#         return phrases,word_code


#     def rolling_hash(self,prev,next,present_hash):
#         next_hash=present_hash
#         for i,prime in  enumerate(prime_nos):
#             next_hash[i]=next_hash[i]-prev
#             next_hash[i]=next_hash[i]/prime
#             next_hash[i]=next_hash[i]+next*math.pow(prime,2)
#         return next_hash

#     def phraseMapping(self,word_code,f):
#         window=deque()
#         indices=[0]*7
#         a=word_code[0]
#         b=word_code[1]
#         c=word_code[2]
#         for i,prime in enumerate(prime_nos):
#             indices[i]=a+b*prime+c*math.pow(prime,2)
#         f.set_bit(1,indices)
#         window.extend([a,b,c])
#         for code in word_code[3:]:
#             x=window.popleft()
#             window.append(code)
#             indices=self.rolling_hash(x,code,indices)
#             f.set_bit(1,indices)


#     def scanInput(self,input_file,input_code,f):
#         ascii_code=0
#         word=''
#         shift_no=0
#         appended=True
#         window=deque()
#         indices=[0]*7
#         prev=''
#         first_letter=True
#         pair=[]
#         for i,c in enumerate(input_file):
#             if 'A'<=c<='Z':
#                 if first_letter:
#                     pair.append(i)
#                     first=False
#                 appended=False
#                 ascii_code=ascii_code+ord(c)-65
#                 word=word+c 
#             else:
#                 if appended is False:
#                     input_code.append(ascii_code)
#                     pair.append(i)
#                     window.append([word,pair])
#                     if len(input_code)==3:
#                         if shift_no==0:
#                             a,b,c=input_code[0],input_code[1],input_code[2];
#                             for i,prime in enumerate(prime_nos):
#                                 indices[i]=a+b*prime+c*math.pow(prime,2)
#                         else:
#                             indices=self.rolling_hash(prev,ascii_code,indices)

#                         if f.look_up(1,indices):
#                             f.set_bit(2,indices)
#                             input_phrases.append(window[0][0]+' '+window[1][0]+' '+window[2][0])
#                             input_phrases_idx.append([window[0][1][0],window[2][1][1]])
#                         prev=input_code.popleft()
#                         window.popleft()
#                         shift_no+=1
#                     ascii_code=0
#                     word=''
#                     appended=True
#                     first_letter=True
#                     pair=[]
#         return input_phrases,input_phrases_idx


#     def filter_word(self,patterns,word_code,f):
#         window = deque()
#         indices = [0]*7
#         a=word_code[0]
#         b=word_code[1]
#         c=word_code[2]
#         for i,prime in enumerate(prime_nos):
#             indices[i] = a + b * prime + c * math.pow(prime, 2)

#         if not f.look_up(2, indices):
#             patterns[0] = ' '
#         window.extend([a, b, c])

#         shift_no = 0
#         # shift_no = 0
#         for code in word_code[3:]:
#             x = window.popleft()
#             window.append(code)
#             shift_no += 1
#             indices=self.rolling_hash(x, code, indices)
#             if not f.look_up(2, indices):
#                 # patterns[shift_no] = ' '
#                 patterns.append(' ')
    

#         patterns = list(filter(lambda x: x != ' ',patterns))
#         return patterns


#     def exactMatching(self,input_phrases,patterns):
#         k=[]
#         A=ahoh()
#         line=' '.join(input_phrases)

#         k=len(patterns)

#         input_phrases,input_phrases_idx=A.searchWords(patterns,k,line)

#         return input_phrases,input_phrases_idx



#     def calc_plag(self,input_phrases,input_phrases_idx):

#         commonwords=[]
#         list1=[]
#         list2=[]
#         length=0
#         prev=0

#         for i,phrase in enumerate(input_phrases):
#             if i==0:
#                 words=phrase.split()
#                 for j in range(3):
#                     commonwords.append(words[j])
#                     list1.append(words[j])
#                 prev=words
#             else:
#                 words=phrase.split()
#                 if input_phrases_idx[i][0]==input_phrases_idx[i-1][1]+2 and (prev[1]==words[0] and prev[2]==words[1]) :
#                     commonwords.append(words[2])
#                     list1.append(words[2])
#                 else:
#                     if (prev[1]!=words[0]):
#                         list2.append(' '.join(list1))
#                         list1=[]
#                     for j in range(3):
#                         commonwords.append(words[j])
#                         list1.append(words[j])
#                 prev=words

#         list2.append(' '.join(list1))

#         print("Sentence:-")

#         # for i in range(len(list2)):
#         #     print(i+1,":",list2[i],".")
#         return commonwords



#     def percentage_calc(self,common_words,src_content,doc_content):
#         src_word=[]
#         doc_word=[]
#         for one_word in src_content.upper().split():
#             letter=one_word[len(one_word)-1]
#             if not 'A' <= letter <= 'Z':
#                 src_word.append(one_word[:len(one_word)-1])
#             else:
#                 src_word.append(one_word)

#         for one_word in doc_content.upper().split():
#             letter=one_word[len(one_word)-1]
#             if not 'A' <= letter <= 'Z':
#                 doc_word.append(one_word[:len(one_word)-1])
#             else:
#                 doc_word.append(one_word)

#         src_size=len(src_word)
#         doc_size=len(doc_word)

#         common_words_set = set(common_words)
#         print(common_words_set)
#         d = len(common_words_set)
#         plagPercent1 = (d/float(src_size)) * 100
#         #plagPercent2 = (d/float(doc_size)) * 100

#         print("Percentage match found between files :",end=' ')
#         print(str(plagPercent1)+"%")
#         #print("Plagiarism Percentage in file 2 :",end=' ')
#         #print(str(plagPercent2)+"%")

#     def source(self,test_text,src_text):
#         # try:
#         # 	with open(filename,'r') as file:
#         # 		src_content=file.read()
#         # 		#print(src_content)
#         # 	with open('search.txt','r') as file:
#         # 		input_content=file.read()
#         # 		#print(input_content)
#         # 	detector(src_content.upper(),input_content.upper())
#         # except IndexError:
#         # 	pass
#         self.detector(test_text,src_text)


#     def search_main(self):
#         # if path.exists("source1.txt"):
#         # 	print("source1.txt")
#         # print(self.test_text)
#         # print(self.source_text)
#         self.source(self.test_text,self.source_text)

#         # else:
#         # 	print("Site is encrypted")

#         # if path.exists("source2.txt"):
            
#         # 	source("source2.txt")
        
#         # else:
#         # 	print("Site is encrypted")

#         # if path.exists("source3.txt"):

#         # 	source("source3.txt")
        
#         # else:
#         # 	print("Site is encrypted")


#         # if path.exists("source4.txt"):

#         # 	source("source4.txt")
        
#         # else:
#         # 	print("Site is encrypted")


#         # if path.exists("source5.txt"):

#         # 	source("source5.txt")	

#         # else:
#         # 	print("Site is encrypted")


# print('second entry')
