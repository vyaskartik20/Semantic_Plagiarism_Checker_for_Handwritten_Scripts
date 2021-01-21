import scipy.sparse as ss
import os
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

def _s_pos_or_zero(x):
    return x if x > 0 else 0

def _s_zero_mask(x, y):
    return 0 if y == 0 else x

def _s_safe_divide(x, y):
    return 0 if x == 0 or y == 0 else x / y

_v_pos_or_zero = np.vectorize(_s_pos_or_zero)
_v_zero_mask = np.vectorize(_s_zero_mask)
_v_safe_divide = np.vectorize(_s_safe_divide)

def _assymetric_subset_measure(doc1, doc2):
    epsilon = np.ones(doc1.shape) * 2
    filtered = _v_pos_or_zero(epsilon - (_v_safe_divide(doc1, doc2) +
    _v_safe_divide(doc2, doc1)))
    zdoc1 = _v_zero_mask(doc1, filtered)
    zdoc2 = _v_zero_mask(doc2, filtered)
    return np.sum(np.dot(zdoc1, zdoc2)) / np.sum(np.dot(doc1, doc2))

def scam_distance(doc1, doc2):
    asm12 = _assymetric_subset_measure(doc1, doc2)
    asm21 = _assymetric_subset_measure(doc2, doc1)
    return min(asm12, asm21)

def main():
    docs = []
    cats = []
    files = []

    for file in os.listdir('docs'):
        fileName = "docs/" + file
        files.append(fileName)
  
    for file in files:
        f = open(file, 'r')
        body = re.sub("\\s+", " ", " ".join(f.readlines()))
        f.close()
        docs.append(body)
        cats.append("X")
    pipeline = Pipeline([
    ("vect", CountVectorizer(min_df=0, stop_words="english")),
    ("tfidf", TfidfTransformer(use_idf=False))])
    tdMatrix = pipeline.fit_transform(docs, cats)
    testDocs = []
    for i in range(0, tdMatrix.shape[0]):
        testDocs.append(np.asarray(tdMatrix[i, :].todense()).reshape(-1))
    
    i=0
    for file1 in (files):
        # print(testDocs[i])
        j=0
        for file2 in (files):
            if(file1 != file2):
                scamDist = scam_distance(testDocs[i], testDocs[j])
                print (f" Plagiarism between {file1} and {file2} is :: {1-scamDist}")
            j=j+1
        i=i+1

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    














 # 2 documents :: -- 


# from __future__ import division

# from operator import itemgetter

# import nltk.cluster.util as nltkutil
# import numpy as np
# import random
# import re
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.pipeline import Pipeline

# def preprocess(fnin, fnout):
#   fin = open(fnin, 'rb')
#   fout = open(fnout, 'wb')
#   buf = []
#   id = ""
#   category = ""
#   for line in fin:
#     line = line.strip()
#     if line.find(b"-- Document Separator --") > -1:
#       if len(buf) > 0:
#         # write out body,
#         body = re.sub("\s+", " ", " ".join(buf))
#         print("%s\t%s\t%s\n" % (id, category, body))
#         fout.write("%s\t%s\t%s\n" % (id, category, body))
#       # process next header and init buf
#       id, category, rest = map(lambda x: x.strip(), line.split(": "))
#       buf = []
#     else:
#       # process body
#       buf.append(line)
#   fin.close()
#   fout.close()

# def train(fnin):
#   docs = []
#   cats = []
#   fin = open(fnin, 'rb')
#   for line in fin:
#     id, category, body = line.strip().split("\t")
#     docs.append(body)
#     cats.append(category)
#   fin.close()
#   pipeline = Pipeline([
#     ("vect", CountVectorizer(min_df=0, stop_words="english")),
#     ("tfidf", TfidfTransformer(use_idf=False))])
#   tdMatrix = pipeline.fit_transform(docs, cats)
#   return tdMatrix, cats

# def test(tdMatrix, cats, fsim):
#   testIds = random.sample(range(0, len(cats)), int(0.1 * len(cats)))
#   testIdSet = set(testIds)
#   refIds = filter(lambda x: x not in testIdSet, range(0, len(cats)))
#   sims = np.zeros((len(testIds), len(refIds)))
#   for i in range(0, len(testIds)):
#     for j in range(0, len(refIds)):
#       doc1 = np.asarray(tdMatrix[testIds[i], :].todense()).reshape(-1)
#       doc2 = np.asarray(tdMatrix[refIds[j], :].todense()).reshape(-1)
#       sims[i, j] = fsim(doc1, doc2)
#   for i in range(0, sims.shape[0]):
#     xsim = list(enumerate(sims[i, :]))
#     sortedSims = sorted(xsim, key=itemgetter(1), reverse=True)[0:5]
#     sourceCat = cats[testIds[i]]
#     numMatchedCats = 0
#     numTestedCats = 0
#     for j, score in sortedSims:
#       targetCat = cats[j]
#       if sourceCat == targetCat:
#         numMatchedCats += 1
#       numTestedCats += 1
#     print("Test Doc: %d, Source Category: %s, Target Matched: %d/%d times" %
#       (i, sourceCat, numMatchedCats, numTestedCats))
      
# def main():
#   preprocess("input1.txt", "input2.txt")
#   tdMatrix, cats = train("input2.txt")
#   print ("Results with Cosine Distance Similarity Measure")
#   test(tdMatrix, cats, nltkutil.cosine_distance)
#   print ("Results with Euclidean Distance Similarity Measure")
#   test(tdMatrix, cats, nltkutil.euclidean_distance)
#   print ("Results with SCAM Distance Similarity Measure")
#   test(tdMatrix, cats, scam_distance)
  
# if __name__ == "__main__":
#   main()