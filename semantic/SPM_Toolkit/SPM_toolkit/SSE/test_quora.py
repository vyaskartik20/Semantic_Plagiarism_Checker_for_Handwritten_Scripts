from __future__ import division
import os
import sys 
import time
import torch
import random
import pickle
from model import *
import torch.nn as nn
from torch import optim
from torch_util import *
from datetime import datetime
from datetime import timedelta
from collections import Counter
from torchtext.vocab import load_word_vectors


import pdb


def create_batch(data,from_index, to_index):
  if to_index > len(data):
    to_index = len(data)
  lsize, rsize = 0, 0
  lsize_list, rsize_list = [], []
  for i in range(from_index, to_index):
    length = len(data[i][0])
    lsize_list.append(length)
    if length > lsize:
      lsize = length
    length = len(data[i][1])
    rsize_list.append(length)
    if length > rsize:
      rsize = length

  left_sents, right_sents, labels = [], [], []
  for i in range(from_index, to_index):
    lsent = data[i][0]
    lsent = lsent + ['<pad>' for k in range(lsize - len(lsent))]
    left_sents.append([word2id[word] for word in lsent])
    rsent = data[i][1]
    rsent = rsent + ['<pad>' for k in range(rsize - len(rsent))]
    right_sents.append([word2id[word] for word in rsent])
    labels.append(data[i][2])

  left_sents=Variable(torch.LongTensor(left_sents))
  right_sents=Variable(torch.LongTensor(right_sents))
  labels=Variable(torch.LongTensor(labels))
  lsize_list=torch.LongTensor(lsize_list)
  rsize_list =torch.LongTensor(rsize_list)

  if torch.cuda.is_available():
    left_sents=left_sents.cuda()
    right_sents=right_sents.cuda()
    labels=labels.cuda()
    lsize_list=lsize_list.cuda()
    rsize_list=rsize_list.cuda()
  return left_sents, right_sents, labels, lsize_list, rsize_list


if __name__ == '__main__':
  task='quora'
  print('task: '+task)
  torch.manual_seed(6)

  num_class = 2
  if torch.cuda.is_available():
    print('CUDA is available!')
  
  basepath = './data'
  test_pairs = readQuoradata(basepath + '/test/', 1000)

  with open(os.path.join('./results', 'vocab.pkl'), 'rb') as f:
    tokens, word2id = pickle.load(f)

  model = StackBiLSTMMaxout(h_size=[512, 1024, 2048], 
                            v_size=len(tokens), 
                            d=300, 
                            mlp_d=1600, 
                            dropout_r=0.1, 
                            max_l=60, 
                            num_class=num_class)


  batch_size=32
  criterion = nn.CrossEntropyLoss()

  ckpt_path = os.path.join('./results', '%s_%d.pkl' % (task, 8))
  model.load_state_dict(torch.load(ckpt_path))
  model.eval()
  if torch.cuda.is_available():
    model.cuda()
  
  # Test
  start_time = time.time()
  test_batch_index = 0
  test_num_correct = 0
  msg = ''
  accumulated_loss = 0
  test_batch_i = 0
  pred = []
  gold = []
  while test_batch_i < len(test_pairs):
    left_sents, right_sents, labels, lsize_list, rsize_list = create_batch(
        test_pairs, test_batch_i, test_batch_i+batch_size)
    left_sents = torch.transpose(left_sents, 0, 1)
    right_sents = torch.transpose(right_sents, 0, 1)
    test_batch_i+=len(labels)
    output = model(left_sents, lsize_list, right_sents, rsize_list)
    result = output.data.cpu().numpy()
    loss = criterion(output, labels)
    # accumulated_loss += loss.data[0]
    accumulated_loss += loss.item()
    a = np.argmax(result, axis=1)
    b = labels.data.cpu().numpy()
    test_num_correct += np.sum(a == b)
  
  elapsed_time = time.time() - start_time
  print('Test finished within ' + str(timedelta(seconds=elapsed_time)))
  msg += '\t test loss: %.4f' % accumulated_loss
  test_acc = test_num_correct / len(test_pairs)
  msg += '\t test accuracy: %.4f' % test_acc
  print(msg)

