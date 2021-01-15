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
  if len(sim_scores) == 0:
    print(0)
  else:
    print(max(sim_scores))

word1 = "fruit"
word2 = "apple"

similarity(word1, word2)