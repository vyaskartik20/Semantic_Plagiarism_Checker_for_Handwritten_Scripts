from bitarray import *
from collections import deque
import ahocorasick as ahc
import math
import os
from os import path
global prime_nos,phrases,word_code,input_phrases,input_phrases_idx
prime_nos=(13,17,19,23,29,31,37)
phrases=[]
word_code=[]
input_phrases=[]
input_phrases_idx=[]


class bloom_filter:
    def __init__(self, size):
        self.size = size
        self.first_filter, self.second_filter = bitarray(size), bitarray(size)
        self.first_filter.setall(0)
        self.second_filter.setall(0)

    def set_bit(self, filter_no, indices):
        for idx in indices:
            if(int(idx) > self.size) :
                continue
            if filter_no == 1:
                self.first_filter[int(idx)] = 1
            else:
                self.second_filter[int(idx)] = 1

    def look_up(self, filter_no, indices):
        for idx in indices:
            if(int(idx) > self.size) :
                continue
            if filter_no == 1 and not self.first_filter[int(idx)]:
                return False
            if filter_no == 2 and not self.second_filter[int(idx)]:
                return False
        return True

    def display(self):
        l=1
        # print(self.first_filter)
        # print(self.second_filter)
        
class ahoh:
    def __init__(self):
        self.maxs=100000
        self.maxc=260
        self.out=[0]*self.maxs
        self.f=[-1]*self.maxs
        self.g=[]

        for i in range(self.maxs):
            self.g.append([])
            for j in range(self.maxc):
                self.g[i].append(-1)

    def buildMatchingMachine(self,arr,k):
        states=1
        for i in range(k):
            word=arr[i]
            currentState=0
            for j in range(len(word)):
                if word[j]!=' ':
                    ch=ord(word[j])-ord('A')
                else:
                    ch=26
                # if(currentState < self.maxs and ch < self.maxc ) :
                # print( 'status      ' + str(currentState) + '      ' + str(ch))
                if(self.g[currentState][ch]==-1):
                    self.g[currentState][ch]=states
                    states+=1
                currentState=self.g[currentState][ch]
            
            if(currentState < self.maxs):
                self.out[currentState] |= (1<<i)

        # for i in range(maxc):
        #print(out)
        for ch in range(self.maxc):
            if (self.g[0][ch]==-1):
                self.g[0][ch]=0
        q=[]

        for ch in range(self.maxc):
            # if(currentState < self.maxs and ch < self.maxc ) :
            if self.g[0][ch]!=0:
                self.f[self.g[0][ch]]=0
                q.append(self.g[0][ch])

        while(len(q)):
            state=q.pop(0)
            for ch in range(self.maxc):
                if(self.g[state][ch]!=-1):
                    failure=self.f[state]
                    while(self.g[failure][ch]==-1):
                        failure=self.f[failure]
                    failure=self.g[failure][ch]
                    self.f[self.g[state][ch]]=failure
                    self.out[self.g[state][ch]] |= self.out[failure]
                    q.append(self.g[state][ch])

        return states

    def findNextState(self,currentState,nextInput):
        answer=currentState
        if nextInput!=' ':
            ch=ord(nextInput)-ord('A')
        else:
            ch=26
        while(self.g[answer][ch]==-1):
            answer=self.f[answer]
        return self.g[answer][ch]

    def searchWords(self,arr,k,text):
        input_phrase=[]
        input_phrases_indx=[]
        self.buildMatchingMachine(arr,k)
        currentState=0
        for i in range(len(text)):
            currentState=self.findNextState(currentState,text[i])
            if(self.out[currentState]==0):
                continue
            for j in range(k):
                if (self.out[currentState] & (1<<j) ):
                    input_phrase.append(arr[j])
                    input_phrases_indx.append([i-len(arr[j])+1,i])
        return input_phrase,input_phrases_indx

class OnlinePlag : 
    
    def __init__(self,test_text, source_text):
        self.test_text = test_text
        self.source_text=source_text
    
    
    def detector(self,patt_file,input_file):
        f=bloom_filter(10000007)
        input_code=deque()

        phrases,word_code=self.convertPhrases(patt_file)

        self.phraseMapping(word_code,f)

        input_phrases,input_phrases_idx=self.scanInput(input_file,input_code,f)

        patterns=self.filter_word(phrases,word_code,f)

        input_phrases,input_phrases_idx=self.exactMatching(input_phrases,patterns)

        commonwords=self.calc_plag(input_phrases,input_phrases_idx)

        return(self.percentage_calc(commonwords,patt_file,input_file))


    def convertPhrases(self,patt_file):
        ascii_code=0
        word=''
        appended=True
        window=deque()
        for c in patt_file:
            if 'A'<=c<'Z':  
                ascii_code=ascii_code+ord(c)-65
                word=word+c
                appended=False
            else: 
                if appended is False:
                    word_code.append(ascii_code)
                    window.append(word)
                    if len(window)==3:
                        k=' '.join(list(window))
                        phrases.append(k)
                        window.popleft()
                    ascii_code=0
                    word=''
                    appended=True
        # print(phrases)
        return phrases,word_code


    def rolling_hash(self,prev,next,present_hash):
        next_hash=present_hash
        for i,prime in  enumerate(prime_nos):
            next_hash[i]=next_hash[i]-prev
            next_hash[i]=next_hash[i]/prime
            next_hash[i]=next_hash[i]+next*math.pow(prime,2)
        return next_hash

    def phraseMapping(self,word_code,f):
        window=deque()
        indices=[0]*7
        a=word_code[0]
        b=word_code[1]
        c=word_code[2]
        for i,prime in enumerate(prime_nos):
            indices[i]=a+b*prime+c*math.pow(prime,2)
        f.set_bit(1,indices)
        window.extend([a,b,c])
        for code in word_code[3:]:
            x=window.popleft()
            window.append(code)
            indices=self.rolling_hash(x,code,indices)
            f.set_bit(1,indices)


    def scanInput(self,input_file,input_code,f):
        ascii_code=0
        word=''
        shift_no=0
        appended=True
        window=deque()
        indices=[0]*7
        prev=''
        first_letter=True
        pair=[]
        for i,c in enumerate(input_file):
            if 'A'<=c<='Z':
                if first_letter:
                    pair.append(i)
                    first=False
                appended=False
                ascii_code=ascii_code+ord(c)-65
                word=word+c 
            else:
                if appended is False:
                    input_code.append(ascii_code)
                    pair.append(i)
                    window.append([word,pair])
                    if len(input_code)==3:
                        if shift_no==0:
                            a,b,c=input_code[0],input_code[1],input_code[2];
                            for i,prime in enumerate(prime_nos):
                                indices[i]=a+b*prime+c*math.pow(prime,2)
                        else:
                            indices=self.rolling_hash(prev,ascii_code,indices)

                        if f.look_up(1,indices):
                            f.set_bit(2,indices)
                            input_phrases.append(window[0][0]+' '+window[1][0]+' '+window[2][0])
                            input_phrases_idx.append([window[0][1][0],window[2][1][1]])
                        prev=input_code.popleft()
                        window.popleft()
                        shift_no+=1
                    ascii_code=0
                    word=''
                    appended=True
                    first_letter=True
                    pair=[]
        return input_phrases,input_phrases_idx


    def filter_word(self,patterns,word_code,f):
        window = deque()
        indices = [0]*7
        a=word_code[0]
        b=word_code[1]
        c=word_code[2]
        for i,prime in enumerate(prime_nos):
            indices[i] = a + b * prime + c * math.pow(prime, 2)

        if not f.look_up(2, indices):
            patterns[0] = ' '
        window.extend([a, b, c])

        shift_no = 0
        # shift_no = 0
        for code in word_code[3:]:
            x = window.popleft()
            window.append(code)
            shift_no += 1
            indices=self.rolling_hash(x, code, indices)
            if not f.look_up(2, indices):
                # patterns[shift_no] = ' '
                patterns.append(' ')
    

        patterns = list(filter(lambda x: x != ' ',patterns))
        return patterns


    def exactMatching(self,input_phrases,patterns):
        k=[]
        A=ahoh()
        line=' '.join(input_phrases)

        k=len(patterns)

        input_phrases,input_phrases_idx=A.searchWords(patterns,k,line)

        return input_phrases,input_phrases_idx



    def calc_plag(self,input_phrases,input_phrases_idx):

        commonwords=[]
        list1=[]
        list2=[]
        length=0
        prev=0

        for i,phrase in enumerate(input_phrases):
            if i==0:
                words=phrase.split()
                for j in range(3):
                    commonwords.append(words[j])
                    list1.append(words[j])
                prev=words
            else:
                words=phrase.split()
                if input_phrases_idx[i][0]==input_phrases_idx[i-1][1]+2 and (prev[1]==words[0] and prev[2]==words[1]) :
                    commonwords.append(words[2])
                    list1.append(words[2])
                else:
                    if (prev[1]!=words[0]):
                        list2.append(' '.join(list1))
                        list1=[]
                    for j in range(3):
                        commonwords.append(words[j])
                        list1.append(words[j])
                prev=words

        list2.append(' '.join(list1))

        # print("Sentence:-")

        # for i in range(len(list2)):
        #     print(i+1,":",list2[i],".")
        return commonwords



    def percentage_calc(self,common_words,src_content,doc_content):
        src_word=[]
        doc_word=[]
        for one_word in src_content.upper().split():
            letter=one_word[len(one_word)-1]
            if not 'A' <= letter <= 'Z':
                src_word.append(one_word[:len(one_word)-1])
            else:
                src_word.append(one_word)

        for one_word in doc_content.upper().split():
            letter=one_word[len(one_word)-1]
            if not 'A' <= letter <= 'Z':
                doc_word.append(one_word[:len(one_word)-1])
            else:
                doc_word.append(one_word)

        src_size=len(src_word)
        doc_size=len(doc_word)

        common_words_set = set(common_words)
        # print(common_words_set)
        d = len(common_words_set)
        plagPercent1 = (d/float(src_size)) * 100
        #plagPercent2 = (d/float(doc_size)) * 100

        # print("Percentage match found between files :",end=' ')
        # print(str(plagPercent1)+"%")
        return (plagPercent1/100)
        #print("Plagiarism Percentage in file 2 :",end=' ')
        #print(str(plagPercent2)+"%")

    def source(self,test_text,src_text):
        # try:
        # 	with open(filename,'r') as file:
        # 		src_content=file.read()
        # 		#print(src_content)
        # 	with open('search.txt','r') as file:
        # 		input_content=file.read()
        # 		#print(input_content)
        # 	detector(src_content.upper(),input_content.upper())
        # except IndexError:
        # 	pass
        return(self.detector(test_text,src_text))


    def search_main(self):
        # if path.exists("source1.txt"):
        # 	print("source1.txt")
        # print(self.test_text)
        # print(self.source_text)
        return(self.source(self.test_text,self.source_text))


# print('second entry')

# object = OnlinePlag(text1,text2)
# object.search_main()

# text1 = "Kartik Vyas studies at IITJ"
# text2 = "Kartik Vyas is an Undergrad student at IITJ"

#working below
# f = open('data1.txt', encoding="utf8")
# file1_data = f.read()
# # print (similarity.returnTable(similarity.report(str(file1_data))))
# text1 = (str(file1_data))

# f = open('data2.txt', encoding="utf8")
# file2_data = f.read()
# # print (similarity.returnTable(similarity.report(str(file1_data))))
# text2 = (str(file2_data))


def create_rabin_karp_1_features(df): 
    rabin_karp_1_values = []

    for i in df.index:
        if df.loc[i,'Class'] != -1:
            # get texts to compare
            answer_text = df.loc[i, 'Text']
            answer_filename = df.loc[i, 'File'] 
            source_filename = answer_filename
            source_filename = "source" + answer_filename[6:]     
            source_df = df.query('File == @source_filename')
            source_text = source_df.iloc[0].at['Text']

            # value = similarity(answer_text, source_text, False)
            object = OnlinePlag(answer_text,source_text)
            value = object.search_main()
            rabin_karp_1_values.append(value)
        else:
            rabin_karp_1_values.append(-1)

    print('rabin_karp_1 features created!')
    return rabin_karp_1_values


# object = OnlinePlag(text1,text2)
# object.search_main()

# print(cosine2(text1,text2))