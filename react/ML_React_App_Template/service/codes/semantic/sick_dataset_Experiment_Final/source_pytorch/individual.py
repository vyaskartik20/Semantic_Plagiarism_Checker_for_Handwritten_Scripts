import os
import torch
from torch import Tensor
# from model import *
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.model import *

from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import cosine_1
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import cosine_2
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import cosine_trigram
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import docism_nltk
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import jaccard_trigram
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import lcs
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import ngram
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import phrase_nltk_1
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import phrase_nltk_2
# from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import rabin_karp_1
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import rabin_karp_2
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import sequence_matcher
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import embed_spacy
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import bert_sentence_encoder


def make_features(text1,text2) : 
    arr = []

    val = bert_sentence_encoder.similarity(text1,text2)
    arr.append(val[0][0])
    
    # print(val)
    # print(val[0])
    # print(val[0][0])
    
    # print('process1')
    
    from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.distinctFeatures import tensorflow_sentence_embedding
    
    val = tensorflow_sentence_embedding.similarity(text1,text2)
    arr.append(val)
    
    # print('process2')
    
    val = embed_spacy.embed(text1,text2)
    arr.append(val)
    
    # print('process3')
    ngram_range = [1,2,3,4]
    
    for n in ngram_range:
        val = ngram.calculate_containment_individual(text1,text2,n)
        arr.append(val)
    
    # print('process4')
    val = docism_nltk.docism(text1,text2)
    arr.append(val)
    # print('process5')
    
    val = cosine_trigram.similarity(text1,text2)
    arr.append(val)
    # print('process6')


    # features_list.append("cosine_1")
    val = cosine_1.cosineSim(text1,text2)
    arr.append(val)
    # print('process7')

    val = cosine_2.cosine2(text1,text2)
    arr.append(val)    
    # print('process8')

    val = jaccard_trigram.similarity(text1,text2)
    arr.append(val)
    # print('process9')

    val = lcs.lcs_norm_word(text1,text2)
    arr.append(val)
    # print('process10')

    # val = phrase_nltk_1.similarity(text1,text2, True)
    # arr.append(val)

    # val = phrase_nltk_2.similarity(text1,text2, False)
    # arr.append(val)

    val = rabin_karp_2.similarity_individual(text1,text2)
    arr.append(val)

    # print('process11')
    val = sequence_matcher.similarity(text1,text2)
    arr.append(val)
    # print('process12')
    # print('process13')

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
    
    PATH = 'codes/semantic/sick_dataset_Experiment_Final/source_pytorch/model/mod.pt'
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
                
                print (result)
                
                yhat = predict(result, model)
                
                print(f"{file1} and {file2}  ::    {yhat}  ")
                # print(result)
                
                # print('Predicted: %.3f' % yhat)
                
                # print()
                        
                        
                        
                        # print (f"the plag between {file1} and {file2} is : :  {result} ")
                    
def web_semantic_similarity(text1, text2) :
    # print('here0')
    PATH = 'D:/BTP_2/react/ML_React_App_Template/service/codes/semantic/sick_dataset_Experiment_Final/source_pytorch/model/mod.pt'
    # PATH = 'model/mod.pt'
    model = torch.load(PATH)
    # print('here1')
    
    result = make_features(text1,text2)
    
    # print('here2')
    
                
    # print (result)
    
    yhat = predict(result, model)
    # print('here3')
    
    return yhat
    # print(f"{file1} and {file2}  ::    {yhat}  ")
                    
if __name__ == '__main__':
    main()