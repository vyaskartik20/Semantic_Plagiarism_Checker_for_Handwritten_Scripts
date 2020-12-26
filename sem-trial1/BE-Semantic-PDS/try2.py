import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM    #CuDNNLSTM
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Bidirectional
from keras.layers.embeddings import Embedding
import pandas as pd
import numpy as np
from numpy import array
from preprocess import Preprocess
from dataloader import dataLoader
from sklearn.feature_extraction.text import TfidfVectorizer
from random import random
from numpy import cumsum
from keras.layers import TimeDistributed
from keras.preprocessing.sequence import pad_sequences
from sklearn.decomposition import TruncatedSVD
import h5py

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

train_filename = "msr_paraphrase_train.txt"
test_filename = "msr_paraphrase_test.txt"
train_labels, train_pair1, train_pair2 = dataLoader(train_filename)
test_labels, test_pair1, test_pair2 = dataLoader(test_filename)
assert len(train_pair1) == len(train_pair2)
assert len(test_pair1) == len(test_pair2)
text = train_pair2 + train_pair1
text = " ".join(text)

preprocess = Preprocess(bigrams=False, vocab_size=8000)
preprocess.build_vocab(text, stem=True)
n = -1
train_pair1 = preprocess.preprocess(train_pair1)[:n]
train_pair2 = preprocess.preprocess(train_pair2)[:n]

test_pair1 = preprocess.preprocess(test_pair1)[:n]
test_pair2 = preprocess.preprocess(test_pair2)[:n]

train_labels = train_labels[:n]
test_labels = test_labels[:n]

# print(train_pair1)
# print(train_pair2)

corpus = train_pair1 + train_pair2

vectorizer = TfidfVectorizer().fit(corpus)

train_vec1 = vectorizer.transform(train_pair1).todense()
train_vec2 = vectorizer.transform(train_pair2).todense()
test_vec1 = vectorizer.transform(test_pair1).todense()
test_vec2 = vectorizer.transform(test_pair2).todense()

# print(train_vec1.shape)

svd = TruncatedSVD(n_components=1000)


def project_vector(vec, fit=False):
    """ Project vector into a low dimension space """
    if fit:
        svd.fit(vec)
    vec = svd.transform(vec)
    return vec


# vectors in low dimension
train_vec1_ldim = project_vector(train_vec1, fit=True)
train_vec2_ldim = project_vector(train_vec2)
test_vec1_ldim = project_vector(test_vec1)
test_vec2_ldim = project_vector(test_vec2)

train_features = np.concatenate((train_vec1_ldim, train_vec2_ldim), axis=1)
test_features = np.concatenate((test_vec1_ldim, test_vec2_ldim), axis=1)

data = pad_sequences(train_features, maxlen=1000)
model = Sequential()
model.add(Embedding(300, 1000, input_length=1000))  #1. 2000 2. 1000 3. input_length=1000
model.add(Bidirectional(LSTM(100, activation='sigmoid', dropout=0.2, recurrent_dropout=0.2)))
# model.add(Dense(1, activation='relu'))    #1. activation='sigmoid'  2. tf.nn.sigmoid  3.relu
model.add(Dense(1, activation='softmax'))
model.summary()

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])  # binary_crossentropy, categorical_crossentropy,
model.fit(data, np.array(train_labels), validation_split=0.2, epochs=1, batch_size=1)  
# epochs=10 2.epochs=25, batch_size=1

model.save('paraphrase.h5')