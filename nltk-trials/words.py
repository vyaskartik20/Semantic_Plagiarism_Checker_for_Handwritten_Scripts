from __future__ import division
from nltk.corpus import wordnet as wn
import sys

def similarity(w1, w2, sim=wn.path_similarity):
  synsets1 = wn.synsets(w1)
  synsets2 = wn.synsets(w2)
  sim_scores = []
  for synset1 in synsets1:
    for synset2 in synsets2:
      # print(synset1, synset2)
      sim_scores.append(sim(synset1, synset2))
  
  # print(sim_scores)
  
  if len(sim_scores) == 0:
    print(0)
  else:
    ans=0    
    for index in sim_scores :
      try : 
        if index > ans :
          ans=index
      except :
        continue
    
    print(ans)


word1 = "play"
word2 = "game"

similarity(word1, word2)