#@title Load the Universal Sentence Encoder's TF Hub module
from absl import logging
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
model = hub.load(module_url)
# print ("module %s loaded" % module_url)
def embed(input):
  return model(input)

def plot_similarity(labels, features, rotation):
  corr = np.inner(features, features)
  # print(corr)
  value = corr[0][1]
  # print (value)
  return value
#   nums = [1,2,3,4,5]
#   sns.set(font_scale=1.2)
#   g = sns.heatmap(
#       corr,
#       xticklabels=nums,
#       yticklabels=nums,
#       vmin=0,
#       vmax=1,
#       cmap="YlOrRd")
#   g.set_xticklabels(labels, rotation=rotation)
#   g.set_title("Semantic Textual Similarity")
#   plt.show()

def run_and_plot(messages_):
  message_embeddings_ = embed(messages_)
  value = plot_similarity(messages_, message_embeddings_, 90)
  return value

def similarity(text1,text2) :
  texts = []
  # folder = "docs2"

  # for x in range(1,9):
  #     with open( folder + "/" +  str(x)+'.txt','r') as file:
  #         Str = file.read()
  #         texts.append(Str)
  
  texts.append(text1)
  texts.append(text2)
          
  value = run_and_plot(texts)
  return value

def create_tensorflow_sentence_embedding_features(df): 
    sequence_matcher_values = []

    for i in df.index:
        if df.loc[i,'Class'] > -1:
            # get texts to compare
            answer_text = df.loc[i, 'Text']
            answer_filename = df.loc[i, 'File'] 
            source_filename = answer_filename
            source_filename = "source" + answer_filename[6:]     
            source_df = df.query('File == @source_filename')
            source_text = source_df.iloc[0].at['Text']

            # value = similarity(answer_text, source_text, False)
            value = similarity(answer_text,source_text)
            
            if value > 1 :
                value =1
            if value < 0 :
                value = 0
            
            sequence_matcher_values.append(value)
        else:
            sequence_matcher_values.append(-1)

    print('tensorflow sentence embeddings features created!')
    return sequence_matcher_values

# answer_text = "kartik vyas is a good boy"
# source_text = "kartik vyas is a student at IITJ"

# value = similarity(answer_text,source_text)
# print(f" the plag is  : {value} ")

# files = os.listdir('docs')

# for file1 in files :
#     file1 = 'docs/' + file1
#     # with open (file1,'r') as fileStr1:
#         # text1 = fileStr1.read()
#     text1 = open(file1, errors='ignore').read()
#     for file2 in files  :
#         file2 = 'docs/' + file2
#         if file1 != file2 :
#             # with open (file2,'r') as fileStr2:
#             text2 = open(file2, errors = 'ignore').read()
#             yhat = similarity(text1,text2)
            
#             print(f"{file1} and {file2}  ::    {yhat}  ")