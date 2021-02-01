import csv
import spacy
import nltk
from itertools import product

# import de_core_news_sm

# nlp = spacy.load('de_core_news_lg')
nlp = spacy.load('en_core_web_lg')

def read_data(data_dir):
    data = []
    with open(data_dir) as tsvin:
        try :
            tsvin = csv.reader(tsvin, delimiter='\t')
            for row in tsvin:
                print(row)
                assert len(row)==3
                data.append((row[0], row[1], row[2]))
        except :
            it=0
    return data


def compare_sentences(text1, text2):
    
    sentences1 = nltk.sent_tokenize(text1)
    sentences2 = nltk.sent_tokenize(text2)
    
    embed1 = []
    embed2 = []
    
    for sentence in sentences1 :
        embedding = nlp(sentence)
        embed1.append(embedding)
        
    for sentence in sentences2 :
        embedding = nlp(sentence)
        embed2.append(embedding)

    totalPlag = 0
    totalEmbeddings = 0
    
    for embedding1 in embed1 :
        simi = 0
        totalEmbeddings = totalEmbeddings + 1
        for embedding2 in embed2:
            sim = embedding1.similarity(embedding2)
            
            if(sim > simi):
                simi = sim
        if(simi > 0.9):
            totalPlag = totalPlag + simi
    
    totalPlag = totalPlag / totalEmbeddings
    return(totalPlag)

        
    # for sen1, sen2 in product(sentences1, sentences2):
    #     sim = sen1.similarity(sen2)
    #     if sim > 0.9:
    #         print('!!!')
    #         print(sim)
    #         print(sen1)
    #         print(sen2)


def get_sim_count(sentences1, sentences2):
    sim_counter = 0
    total = 0
    for sen1 in (sentences1):
        print(sen1)
        for sen2 in (sentences2):
            # print('yessy')
            print('trial    ' + str(sen2))
            total = total + 1
            sim = sen1.similarity(sen2)
            if sim > 0.95:
                sim_counter = sim_counter + 1
    print(f"the total possibilities are {total}")
    return (sim_counter)


def is_plag(text1, text2):
    
    return(compare_sentences(text1,text2))
    
    # sentences1 = (nlp(text1)).sents
    # s1copy = (nlp(text1)).sents
    # sentences2 = (nlp(text2)).sents
    # sim_count = get_sim_count(sentences1, sentences2)
    # # return sim_count
    # number_sentences_in_text1 = sum(1 for _ in s1copy)
    # # number_sentences_in_text1 = sum(1 for _ in s1copy)
    # if (number_sentences_in_text1 * 0.8) <= sim_count:
    #     return 'True, number of sentences in text1 : ' + str(number_sentences_in_text1), 'similarity count: ' + str(sim_count)
    # else:
    #     return 'False, number of sentences in text1 : ' + str(number_sentences_in_text1), 'similarity count: ' + str(sim_count)

import os

files = os.listdir('docs')

for file1 in files :
    file1 = 'docs/' + file1
    with open (file1,'r') as fileStr1:
        text1 = fileStr1.read()
        for file2 in files  :
            file2 = 'docs/' + file2
            if file1 != file2 :
                with open (file2,'r') as fileStr2:
                    text2 = fileStr2.read()
                    result = is_plag(text1,text2)
                    print (f"the plag between {file1} and {file2} is : :  {result} ")

    print()
    print()
    
# data = read_data('train_plag_data.txt')

# count = 0
# plags = []
# no_plags = []
# for i in range(data.__len__()):
#     count = count+1
#     triple = data.pop(0)
#     kind = int(triple.__getitem__(0))
#     is_a_plag = is_plag(triple.__getitem__(1), triple.__getitem__(2))
#     if kind == 1:
#         plags.append(('article pair: ' + str(count), 'is_a_plag: ' + str(is_a_plag)))
#     else:
#         if kind == 0:
#             no_plags.append(('article pair: ' + str(count), 'is_a_plag: ' + str(is_a_plag)))

#     #compare_sentences(triple.__getitem__(1), triple.__getitem__(2))


# print('Plagiarisms are: ')
# print(plags)

# print('Not a Plagiarism is: ')
# print(no_plags)

# ''' Not a Plagiarism = 0 '''
# ''' Not a Plagiarism = 1 '''
