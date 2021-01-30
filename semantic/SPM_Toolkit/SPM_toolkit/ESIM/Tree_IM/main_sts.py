from __future__ import division
import sys

import gc
import numpy
import torch
import time
from data_iterator import TextIterator
import cPickle as pkl
from model_batch import *
from os.path import expanduser
from datetime import timedelta
from numpy import linalg as LA
from torchtext.vocab import load_word_vectors

def pearson(x,y):
	x=np.array(x)
	y=np.array(y)
	x=x-np.mean(x)
	y=y-np.mean(y)
	return x.dot(y)/(LA.norm(x)*LA.norm(y))

# batch preparation
def prepare_data(group_x, group_y, labels):
	lengths_x = [len(s[0]) for s in group_x]
	lengths_y = [len(s[0]) for s in group_y]

	n_samples = len(group_x)
	maxlen_x = numpy.max(lengths_x)
	maxlen_y = numpy.max(lengths_y)

	x_seq = numpy.zeros((maxlen_x, n_samples)).astype('int64')
	y_seq = numpy.zeros((maxlen_y, n_samples)).astype('int64')
	x_mask = numpy.zeros((maxlen_x, n_samples)).astype('float32')
	y_mask = numpy.zeros((maxlen_y, n_samples)).astype('float32')
	x_left_mask = numpy.zeros((maxlen_x, n_samples, maxlen_x)).astype('float32')
	x_right_mask = numpy.zeros((maxlen_x, n_samples, maxlen_x)).astype('float32')
	y_left_mask = numpy.zeros((maxlen_y, n_samples, maxlen_y)).astype('float32')
	y_right_mask = numpy.zeros((maxlen_y, n_samples, maxlen_y)).astype('float32')
	l = numpy.zeros((n_samples, 6)).astype('float32')

	for idx, [s_x, s_y, ll] in enumerate(zip(group_x, group_y, labels)):
		x_seq[-lengths_x[idx]:, idx] = s_x[0]
		x_mask[-lengths_x[idx]:, idx] = 1.
		x_left_mask[-lengths_x[idx]:, idx, -lengths_x[idx]:] = s_x[1]
		x_right_mask[-lengths_x[idx]:, idx, -lengths_x[idx]:] = s_x[2]
		y_seq[-lengths_y[idx]:, idx] = s_y[0]
		y_mask[-lengths_y[idx]:, idx] = 1.
		y_left_mask[-lengths_y[idx]:, idx, -lengths_y[idx]:] = s_y[1]
		y_right_mask[-lengths_y[idx]:, idx, -lengths_y[idx]:] = s_y[2]
		l[idx] = ll

	if torch.cuda.is_available():
		x_seq=Variable(torch.LongTensor(x_seq)).cuda()
		y_seq = Variable(torch.LongTensor(y_seq)).cuda()
		x_mask = Variable(torch.FloatTensor(x_mask)).cuda()
		y_mask = Variable(torch.FloatTensor(y_mask)).cuda()
		x_left_mask=Variable(torch.FloatTensor(x_left_mask)).cuda()
		y_left_mask=Variable(torch.FloatTensor(y_left_mask)).cuda()
		x_right_mask=Variable(torch.FloatTensor(x_right_mask)).cuda()
		y_right_mask=Variable(torch.FloatTensor(y_right_mask)).cuda()
		l=Variable(torch.FloatTensor(l)).cuda()
	else:
		x_seq = Variable(torch.LongTensor(x_seq))
		y_seq = Variable(torch.LongTensor(y_seq))
		x_mask = Variable(torch.FloatTensor(x_mask))
		y_mask = Variable(torch.FloatTensor(y_mask))
		x_left_mask = Variable(torch.FloatTensor(x_left_mask))
		y_left_mask = Variable(torch.FloatTensor(y_left_mask))
		x_right_mask = Variable(torch.FloatTensor(x_right_mask))
		y_right_mask = Variable(torch.FloatTensor(y_right_mask))
		l = Variable(torch.FloatTensor(l))

	x = (x_seq, x_mask, x_left_mask, x_right_mask)
	y = (y_seq, y_mask, y_left_mask, y_right_mask)

	return x, y, l

#label conversion for STS dataset
def label_convertion(y):
	labels = []
	for sim in y:
		sim=float(sim)
		ceil = int(math.ceil(sim))
		floor = int(math.floor(sim))
		tmp = [0, 0, 0, 0, 0, 0]
		if floor != ceil:
			tmp[ceil] = sim - math.floor(sim)
			tmp[floor] = math.ceil(sim) - sim
		else:
			tmp[floor] = 1
		labels.append(tmp)
	return labels

print('task: sts')
print('model: Tree_IM')
if torch.cuda.is_available():
	print('CUDA is available!')
	base_path = expanduser("~") + '/pytorch/DeepPairWiseWord/data/sts'
	embedding_path = expanduser("~") + '/pytorch/DeepPairWiseWord/VDPWI-NN-Torch/data/glove'
else:
	base_path = expanduser("~") + '/Documents/research/pytorch/DeepPairWiseWord/data/sts'
	embedding_path = expanduser("~") + '/Documents/research/pytorch/DeepPairWiseWord/VDPWI-NN-Torch/data/glove'

datasets = [base_path+'/train/a.btree',
            base_path+'/train/b.btree',
            base_path+'/train/sim.txt']
test_datasets = [base_path+'/test/a.btree',
                 base_path+'/test/b.btree',
                 base_path+'/test/sim.txt']
dictionary = base_path+'/sts_vocab_cased.pkl'

maxlen=100
batch_size=32
max_epochs=1000
dim_word=300
with open(dictionary, 'rb') as f:
	worddicts = pkl.load(f)
n_words=len(worddicts)
wv_dict, wv_arr, wv_size = load_word_vectors(embedding_path, 'glove.840B', dim_word)
pretrained_emb=norm_weight(n_words, dim_word)
for word in worddicts.keys():
	try:
		pretrained_emb[worddicts[word]]=wv_arr[wv_dict[word]].numpy()
	except:
		pretrained_emb[worddicts[word]] = torch.normal(torch.zeros(dim_word),std=1).numpy()
print('load data...')
train = TextIterator(datasets[0], datasets[1], datasets[2],
						 dictionary,
						 n_words=n_words,
						 batch_size=batch_size,
						 maxlen=maxlen, shuffle=True)
test = TextIterator(test_datasets[0], test_datasets[1], test_datasets[2],
					 dictionary,
					 n_words=n_words,
					 batch_size=batch_size,
					 shuffle=False)
criterion=torch.nn.KLDivLoss()
#criterion = torch.nn.CrossEntropyLoss()
model = ESIM(dim_word, 6, n_words, dim_word, pretrained_emb)
if torch.cuda.is_available():
	model = model.cuda()
	criterion = criterion.cuda()
optimizer = torch.optim.Adam(model.parameters(),lr=0.0004)
print('start training...')
clip_c=10
max_result=0
report_interval=1000
for epoch in xrange(max_epochs):
	model.train()
	print('--' * 20)
	start_time = time.time()
	batch_counter=0
	train_batch_i = 0
	train_sents_scaned = 0
	train_num_correct = 0
	accumulated_loss=0
	for x1, x2, y in train:
		#print(x1[0][0])
		#for item in x1[0][0]:
		#	print(worddicts.keys()[item])
		y = label_convertion(y)
		x1, x2, y = prepare_data(x1, x2, y)
		train_sents_scaned += len(y)
		optimizer.zero_grad()
		#if x1[0].size(0)>100:
		#	print(x1[0].size(0))
		#continue
		output = F.log_softmax(model(x1[0], x1[1], x1[2], x1[3], x2[0], x2[1], x2[2], x2[3]))
		#result = output.data.cpu().numpy()
		#a = np.argmax(result, axis=1)
		#b = y.data.cpu().numpy()
		#train_num_correct += np.sum(a == b)
		loss = criterion(output, y)
		loss.backward()
		grad_norm = 0.
		''''''
		for m in list(model.parameters()):
			grad_norm+=m.grad.data.norm() ** 2

		for m in list(model.parameters()):
			if grad_norm>clip_c**2:
				try:
					m.grad.data= m.grad.data / torch.sqrt(grad_norm) * clip_c
				except:
					pass
		''''''
		optimizer.step()
		accumulated_loss += loss.data[0]
		batch_counter += 1
		del x1,x2,y
		if batch_counter % report_interval == 0:
			gc.collect()
			msg = '%d completed epochs, %d batches' % (epoch, batch_counter)
			msg += '\t training batch loss: %f' % (accumulated_loss / train_sents_scaned)
			#msg += '\t train accuracy: %f' % (train_num_correct / train_sents_scaned)
			print(msg)
	msg = '%d completed epochs, %d batches' % (epoch, batch_counter)
	msg += '\t training batch loss: %f' % (accumulated_loss / train_sents_scaned)
	# msg += '\t train accuracy: %f' % (train_num_correct / train_sents_scaned)
	print(msg)
	# test after each epoch
	model.eval()
	msg = '%d completed epochs, %d batches' % (epoch, batch_counter)
	accumulated_loss = 0
	dev_num_correct = 0
	n_done = 0
	pred=[]
	gold = []
	for dev_x1, dev_x2, dev_y in test:
		y = label_convertion(dev_y)
		x1, x2, y = prepare_data(dev_x1, dev_x2, y)
		#if x1[0].size(0)>100:
		#	print(x1[0].size(0))
		#continue
		with torch.no_grad():
			output = F.softmax(model(x1[0], x1[1], x1[2], x1[3], x2[0], x2[1], x2[2], x2[3]))
		n_done += len(y)
		result = output.data.cpu().numpy()
		loss = criterion(F.log_softmax(output), y)
		accumulated_loss += loss.data[0]
		a = numpy.argmax(result, axis=1)
		b = y.data.cpu().numpy()
		pred.extend(0 * result[:, 0] + 1 * result[:, 1] + 2 * result[:, 2] + 3 * result[:, 3] + 4 * result[:, 4] + 5 * result[:,5])
		gold.extend(0 * b[:, 0] + 1 * b[:, 1] + 2 * b[:, 2] + 3 * b[:, 3] + 4 * b[:, 4] + 5 * b[:, 5])
	msg += '\t test loss: %f' % (accumulated_loss / n_done)
	dev_acc = dev_num_correct / n_done
	#msg += '\t test accuracy: %f' % dev_acc
	print(msg)
	result1 = pearson(pred[0:450], gold[0:450])
	result2 = pearson(pred[450:750], gold[450:750])
	result3 = pearson(pred[750:1500], gold[750:1500])
	result4 = pearson(pred[1500:2250], gold[1500:2250])
	result5 = pearson(pred[2250:3000], gold[2250:3000])
	result6 = pearson(pred[3000:3750], gold[3000:3750])
	wt_mean = 0.12 * result1 + 0.08 * result2 + 0.2 * result3 + 0.2 * result4 + 0.2 * result5 + 0.2 * result6
	print('weighted pearson mean: %.6f' % wt_mean)
	if wt_mean>max_result:
		max_result=wt_mean
		with open(base_path+'/sts_Tree_IM_prob.txt','w') as f:
			for item in pred:
				f.writelines(str(item)+'\n')
	elapsed_time = time.time() - start_time
	print('Epoch ' + str(epoch) + ' finished within ' + str(timedelta(seconds=elapsed_time)))