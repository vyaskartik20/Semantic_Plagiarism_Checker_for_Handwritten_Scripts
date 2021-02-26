import csv
import spacy
import nltk
from itertools import product
nlp = spacy.load('en_core_web_lg')

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
        if(simi > 0.85):
            totalPlag = totalPlag + simi
    
    totalPlag = totalPlag / totalEmbeddings
    return(totalPlag)

def embed(text1, text2):
        return(compare_sentences(text1,text2))

# for file1 in files :
#     file1 = 'docs/' + file1
#     with open (file1,'r') as fileStr1:
#         text1 = fileStr1.read()
#         for file2 in files  :
#             file2 = 'docs/' + file2
#             if file1 != file2 :
#                 with open (file2,'r') as fileStr2:
#                     text2 = fileStr2.read()
#                     result = is_plag(text1,text2)
#                     print (f"the plag between {file1} and {file2} is : :  {result} ")

def create_embed_spacy_features(df): 
    docism_nltk_values = []
   
    for i in df.index:
        if df.loc[i,'Class'] > -1:
            # get texts to compare
            answer_text = df.loc[i, 'Text']
            answer_filename = df.loc[i, 'File'] 
            source_filename = answer_filename
            source_filename = "source" + answer_filename[6:]     
            source_df = df.query('File == @source_filename')
            source_text = source_df.iloc[0].at['Text']

            cosineValue = embed(answer_text, source_text)
            
            if cosineValue > 1 :
                cosineValue =1
            if cosineValue < 0 :
                cosineValue = 0
            
            docism_nltk_values.append(cosineValue)
        else:
            docism_nltk_values.append(-1)

    print('embed_spacy features created!')
    return docism_nltk_values

