import os
import torch
from torch import Tensor
from model import *

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
from distinctFeatures import tensorflow_sentence_embedding
from distinctFeatures import embed_spacy

def make_features(text1,text2) : 
    arr = []
    
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
    # convert row to data
    row = Tensor([row])
    # make prediction
    yhat = model(row)
    # retrieve numpy array
    yhat = yhat.detach().numpy()
    return yhat

def main() :
    
    files = os.listdir('docs')
    
    PATH = 'model/mod.pt'
    model = torch.load(PATH)
    
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
                
                yhat = predict(result, model)
                
                print(f"{file1} and {file2}  ::    {yhat}  ")
                # print(result)
                
                # print('Predicted: %.3f' % yhat)
                
                # print()
                        
                        
                        
                        # print (f"the plag between {file1} and {file2} is : :  {result} ")
                    
                    
if __name__ == '__main__':
    main()