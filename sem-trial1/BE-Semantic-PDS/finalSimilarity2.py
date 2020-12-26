from __future__ import division
import nltk
import nltk.cluster
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import math
import gensim
#from gensim.models.doc2vec import TaggedDocument
from nltk.tag.stanford import StanfordNERTagger
import os
import re
import pandas as pd
import tensorflow as tf
import csv
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import csv
import numpy as np
import h5py
import keras.models
from random import randint
from nltk.tokenize import word_tokenize


#!wget 'https://nlp.stanford.edu/software/stanford-ner-2018-10-16.zip'
#!unzip stanford-ner-2018-10-16.zip

def lsa():
    java_path = "C:/Program Files/Java/jdk-12/bin/java.exe"
    os.environ['JAVAHOME'] = java_path

    stopwords_en = stopwords.words("english")

    def preprocessing(raw):
        wordlist = nltk.word_tokenize(raw)
        text = [w for w in wordlist if w not in stopwords_en]
        return text
    global text1
    f1 = open('input.txt', 'r', encoding="utf8")
    text1 = preprocessing(f1.read())
    global text2
    f2 = open('cp.txt', 'r', encoding="utf8")   #suspect.txt
    text2 = preprocessing(f2.read())

    st = StanfordNERTagger('stanford_ner/' + 'classifiers/english.muc.7class.distsim.crf.ser.gz',
                           'stanford_ner/' + 'stanford-ner-3.9.2.jar',
                           encoding='utf-8')
    ner = [st.tag(text2) for sent in text2]

    #extract named entities
    named_entities= []
    for sentence in ner:
        temp_entity_name = ''
        temp_named_entity = None
        for text,tag in sentence:
            if tag == 'O':
                temp_entity_name = ' '.join([temp_entity_name, text]).strip() #get NE name
                temp_named_entity = (temp_entity_name, tag)  # get NE and its category
            else:
                if temp_named_entity:
                    named_entities.append(temp_named_entity)
                    temp_entity_name = ''
                    temp_named_entity = None

    #get unique named entities
    named_entities = list(set(named_entities))

    #store named entities in a dataframe
    entity_frame = pd.DataFrame(named_entities,columns=['Entity Name', 'Entity Type'])
    print(entity_frame)
    del entity_frame['Entity Type']
    entity_frame.to_csv(r"suspect_out.txt", header=None, index=None, sep=' ', mode='a', quoting=csv.QUOTE_NONE, escapechar=' ')

    #LSA for corpus
    global file_content
    file_content = open("cp.txt", encoding="utf8").read()   #suspect.txt
    vectorizer = TfidfVectorizer(stop_words='english', smooth_idf=True, ngram_range=(1, 3))
    file_content = file_content.split("\n")
    # print(file_content)
    X = vectorizer.fit_transform(file_content)
    X.shape
    svd_model = TruncatedSVD(n_components=20, algorithm='randomized', n_iter=100, random_state=122)
    svd_model.fit(X)
    len(svd_model.components_)
    terms = vectorizer.get_feature_names()

    for i, comp in enumerate(svd_model.components_):
        terms_comp = zip(terms, comp)
        sorted_terms = sorted(terms_comp, key=lambda x:  x[1], reverse=True)[:7]
        print("\nTopic "+str(i)+": ")
        for t in sorted_terms:
            print(t[0])
            # print(" ")

    #LSA for input
    print("sample input")
    file_content2 = open("input.txt", encoding="utf8").read()
    file_content2 = [file_content2]
    y = vectorizer.transform(file_content2)
    y.shape
    svd_model2 = TruncatedSVD(n_components=20, algorithm='randomized', n_iter=100, random_state=122)
    svd_model2.fit(y)
    len(svd_model2.components_)
    terms2 = vectorizer.get_feature_names()
    for i, comp2 in enumerate(svd_model2.components_):
        terms_comp2 = zip(terms2, comp2)
        sorted_terms2 = sorted(terms_comp2, key=lambda x:  x[1], reverse=True)[:7]
        print("\nTopic "+str(i)+": ")
        for t2 in sorted_terms2:
            print(t2[0])

    print("COSINE")
    cos_sim = cosine_similarity(X, y)
    print(cos_sim)
    #return cos_sim

    #add new code here

    #file_content = open("suspect.txt", encoding="utf8").read()
    #file_content2 = open("input.txt", encoding="utf8").read()

    with open("input.txt", encoding="utf-8") as sent_1:
        content1 = sent_1.readlines()
    a = content1[0].split()
    print(a)

    with open("cp.txt", encoding="utf-8") as sent_2:
        content2 = sent_2.readlines()
    b = content2[0].split()
    print(b)

    # tokenization
    X_list = a
    Y_list = b

    # sw contains the list of stopwords
    sw = stopwords.words('english')
    l1 = [];
    l2 = []

    # remove stop words from string
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}

    # form a set containing keywords of both strings
    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0
    # cosine formula
    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)

    print("Similarity: ", cosine)
    return cosine


def doc_sim():
    # Document similarity
    word_set = set(text1).union(set(text2))
    print(word_set)

    freqd_text1 = FreqDist(text1)
    text1_count_dict = dict.fromkeys(word_set, 0)
    for word in text1:
        text1_count_dict[word] = freqd_text1[word]

    freqd_text2 = FreqDist(text2)
    text2_count_dict = dict.fromkeys(word_set, 0)
    for word in text2:
        text2_count_dict[word] = freqd_text2[word]

    # TF CALCULATIONS
    freqd_text1 = FreqDist(text1)
    text1_length = len(text1)
    text1_tf_dict = dict.fromkeys(word_set, 0)
    for word in text1:
        text1_tf_dict[word] = freqd_text1[word] / text1_length

    freqd_text2 = FreqDist(text2)
    text2_length = len(text2)
    text2_tf_dict = dict.fromkeys(word_set, 0)
    for word in text2:
        text2_tf_dict[word] = freqd_text2[word] / text2_length

    # IDF CALCULATIONS
    text12_idf_dict = dict.fromkeys(word_set, 0)
    text12_length = 2
    for word in text12_idf_dict.keys():
        if word in text1:
            text12_idf_dict[word] += 1
        if word in text2:
            text12_idf_dict[word] += 1

    for word, val in text12_idf_dict.items():
        text12_idf_dict[word] = 1 + math.log(text12_length / (float(val)))

    # TF-IDF CALCULATIONS
    text1_tfidf_dict = dict.fromkeys(word_set, 0)
    for word in text1:
        text1_tfidf_dict[word] = (text1_tf_dict[word]) * (text12_idf_dict[word])
    text2_tfidf_dict = dict.fromkeys(word_set, 0)
    for word in text2:
        text2_tfidf_dict[word] = (text2_tf_dict[word]) * (text12_idf_dict[word])

    v1 = list(text1_tfidf_dict.values())
    v2 = list(text2_tfidf_dict.values())
    similarity = 1 - nltk.cluster.util.cosine_distance(v1, v2)
    print("Similarity Index: {:4.2f} %".format(similarity * 100))
    return similarity*100


def paraphrase():
    fileContent = open("cp.txt", encoding="utf8").read()
    fileContent2 = open("input.txt", encoding="utf8").read()    #s.txt
    fileContent = [fileContent]
    fileContent2 = [fileContent2]
    vectorizer = TfidfVectorizer()
    vec1 = vectorizer.fit_transform(fileContent).toarray()
    vec2 = vectorizer.fit_transform(fileContent2).toarray()
    # print(vec2.shape)
    vec_features = np.concatenate((vec1, vec2), axis=1)
    # print(vec_features.shape)
    model = keras.models.load_model("trial1.h5")
    prediction = model.predict_classes([vec_features])
    print(prediction)
    return prediction

#lsa()

#doc_sim()
#paraphrase()