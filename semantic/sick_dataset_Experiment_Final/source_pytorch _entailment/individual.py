import os
# import torch
# from torch import Tensor
# from model import *
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from keras.models import model_from_json
from numpy import array
import numpy as np

from distinctFeatures import cosine_1
from distinctFeatures import cosine_2
from distinctFeatures import cosine_trigram
from distinctFeatures import docism_nltk
from distinctFeatures import jaccard_trigram
from distinctFeatures import lcs
from distinctFeatures import ngram
from distinctFeatures import phrase_nltk_1
from distinctFeatures import phrase_nltk_2
# from distinctFeatures import rabin_karp_1
from distinctFeatures import rabin_karp_2
from distinctFeatures import sequence_matcher
from distinctFeatures import embed_spacy
from distinctFeatures import bert_sentence_encoder


def make_features(text1,text2) : 
    arr = []

    val = bert_sentence_encoder.similarity(text1,text2)
    arr.append(val[0][0])
    
    # print(val)
    # print(val[0])
    # print(val[0][0])
    
    
    from distinctFeatures import tensorflow_sentence_embedding
    
    val = tensorflow_sentence_embedding.similarity(text1,text2)
    arr.append(val)
    
    val = embed_spacy.embed(text1,text2)
    arr.append(val)
    
    ngram_range = [1,2,3,4]
    
    for n in ngram_range:
        val = ngram.calculate_containment_individual(text1,text2,n)
        arr.append(val)
    
    val = docism_nltk.docism(text1,text2)
    arr.append(val)
    
    val = cosine_trigram.similarity(text1,text2)
    arr.append(val)


    # features_list.append("cosine_1")
    val = cosine_1.cosineSim(text1,text2)
    arr.append(val)

    val = cosine_2.cosine2(text1,text2)
    arr.append(val)    

    val = jaccard_trigram.similarity(text1,text2)
    arr.append(val)

    val = lcs.lcs_norm_word(text1,text2)
    arr.append(val)

    # val = phrase_nltk_1.similarity(text1,text2, True)
    # arr.append(val)

    # val = phrase_nltk_2.similarity(text1,text2, False)
    # arr.append(val)

    val = rabin_karp_2.similarity_individual(text1,text2)
    arr.append(val)

    val = sequence_matcher.similarity(text1,text2)
    arr.append(val)

    return arr

def predict(row, model):
    # make prediction
    row = np.array(row)
    row = row.reshape(-1,15)
    yhat = np.argmax(model.predict(row), axis=-1)
    return yhat

def main() :
    
    files = os.listdir('docs')
    
    # PATH = 'model/mod.pt'
    # model = torch.load(PATH)

    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("model.h5")
    print("Loaded model from disk")
    model.compile(loss='categorical_crossentropy',
                        optimizer='adam', metrics=['accuracy'])
    
    for file1 in files :
        file1 = 'docs/' + file1
        # with open (file1,'r') as fileStr1:
            # text1 = fileStr1.read()
        text1 = open(file1, errors='ignore').read()
        for file2 in files  :
            file2 = 'docs/' + file2
            if file1 != file2 :
                # with open (file2,'r') as fileStr2:
                text2 = open(file2, errors = 'ignore').read()
                result = make_features(text1,text2)
                
                print (result)
                
                yhat = predict(result, model)
                
                print(f"{file1} and {file2}  ::    {yhat}  ")
                # print(result)
                
                # print('Predicted: %.3f' % yhat)
                
                # print()
                        
                        
                        
                        # print (f"the plag between {file1} and {file2} is : :  {result} ")
                    
                    
if __name__ == '__main__':
    main()