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