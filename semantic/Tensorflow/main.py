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
  print(corr)
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
  plot_similarity(messages_, message_embeddings_, 90)


texts = []
folder = "docs2"

for x in range(1,9):
    with open( folder + "/" +  str(x)+'.txt','r') as file:
        Str = file.read()
        texts.append(Str)
        
run_and_plot(texts)
