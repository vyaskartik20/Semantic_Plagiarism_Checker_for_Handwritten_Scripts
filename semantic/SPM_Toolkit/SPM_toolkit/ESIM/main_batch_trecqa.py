from __future__ import division
import sys
from data_iterator import TextIterator
import cPickle as pkl
from os.path import expanduser
import torch
import numpy
from model_batch import *
import time
import os
from datetime import timedelta
from torchtext.vocab import load_word_vectors

# batch preparation
# batch preparation
def prepare_data(seqs_x, seqs_y, labels, maxlen=None):
	lengths_x = [len(s) for s in seqs_x]
	lengths_y = [len(s) for s in seqs_y]

	if maxlen is not None:
		new_seqs_x = []
		new_seqs_y = []
		new_lengths_x = []
		new_lengths_y = []
		new_labels = []
		for l_x, s_x, l_y, s_y, l in zip(lengths_x, seqs_x, lengths_y, seqs_y, labels):
			if l_x < maxlen and l_y < maxlen:
				new_seqs_x.append(s_x)
				new_lengths_x.append(l_x)
				new_seqs_y.append(s_y)
				new_lengths_y.append(l_y)
				new_labels.append(l)
		lengths_x = new_lengths_x
		seqs_x = new_seqs_x
		lengths_y = new_lengths_y
		seqs_y = new_seqs_y
		labels = new_labels

		if len(lengths_x) < 1 or len(lengths_y) < 1:
			return None, None, None, None, None

	n_samples = len(seqs_x)
	maxlen_x = numpy.max(lengths_x)
	maxlen_y = numpy.max(lengths_y)

	x = numpy.zeros((maxlen_x, n_samples)).astype('int64')
	y = numpy.zeros((maxlen_y, n_samples)).astype('int64')
	x_mask = numpy.zeros((maxlen_x, n_samples)).astype('float32')
	y_mask = numpy.zeros((maxlen_y, n_samples)).astype('float32')
	l = numpy.zeros((n_samples,)).astype('int64')
	for idx, [s_x, s_y, ll] in enumerate(zip(seqs_x, seqs_y, labels)):
		x[:lengths_x[idx], idx] = s_x
		x_mask[:lengths_x[idx], idx] = 1.
		y[:lengths_y[idx], idx] = s_y
		y_mask[:lengths_y[idx], idx] = 1.
		l[idx] = ll

	if torch.cuda.is_available():
		x=Variable(torch.LongTensor(x)).cuda()
		x_mask=Variable(torch.Tensor(x_mask)).cuda()
		y=Variable(torch.LongTensor(y)).cuda()
		y_mask=Variable(torch.Tensor(y_mask)).cuda()
		l=Variable(torch.LongTensor(l)).cuda()
	else:
		x = Variable(torch.LongTensor(x))
		x_mask = Variable(torch.FloatTensor(x_mask))
		y = Variable(torch.LongTensor(y))
		y_mask = Variable(torch.FloatTensor(y_mask))
		l = Variable(torch.LongTensor(l))
	return x, x_mask, y, y_mask, l

# some utilities
def ortho_weight(ndim):
	"""
	Random orthogonal weights

	Used by norm_weights(below), in which case, we
	are ensuring that the rows are orthogonal
	(i.e W = U \Sigma V, U has the same
	# of rows, V has the same # of cols)
	"""
	W = numpy.random.randn(ndim, ndim)
	u, s, v = numpy.linalg.svd(W)
	return u.astype('float32')


def norm_weight(nin, nout=None, scale=0.01, ortho=True):
	"""
	Random weights drawn from a Gaussian
	"""
	if nout is None:
		nout = nin
	if nout == nin and ortho:
		W = ortho_weight(nin)
	else:
		W = scale * numpy.random.randn(nin, nout)
	return W.astype('float32')

if torch.cuda.is_available():
	print('CUDA is available!')
	base_path = expanduser("~") + '/pytorch/ESIM'
	embedding_path = expanduser("~") + '/pytorch/DeepPairWiseWord/VDPWI-NN-Torch/data/glove'
else:
	base_path = expanduser("~") + '/Documents/research/pytorch/ESIM'
	embedding_path = expanduser("~") + '/Documents/research/pytorch/DeepPairWiseWord/VDPWI-NN-Torch/data/glove'

task='trecqa'
print('task: '+task)
if task=='snli':
	dictionary=base_path+'/data/word_sequence/snli_vocab_cased.pkl'
	datasets         = [base_path+'/data/word_sequence/premise_snli_1.0_train.txt',
							base_path+'/data/word_sequence/hypothesis_snli_1.0_train.txt',
							base_path+'/data/word_sequence/label_snli_1.0_train.txt']
	valid_datasets   = [base_path+'/data/word_sequence/premise_snli_1.0_dev.txt',
							base_path+'/data/word_sequence/hypothesis_snli_1.0_dev.txt',
							base_path+'/data/word_sequence/label_snli_1.0_dev.txt']
	test_datasets    = [base_path+'/data/word_sequence/premise_snli_1.0_test.txt',
							base_path+'/data/word_sequence/hypothesis_snli_1.0_test.txt',
							base_path+'/data/word_sequence/label_snli_1.0_test.txt']
elif task=='mnli':
	dic = {'entailment': '0', 'neutral': '1', 'contradiction': '2'}
	dictionary = base_path + '/data/word_sequence/mnli_vocab_cased.pkl'
	datasets = [base_path + '/data/word_sequence/premise_multinli_1.0_train.txt',
				base_path + '/data/word_sequence/hypothesis_multinli_1.0_train.txt',
				base_path + '/data/word_sequence/label_multinli_1.0_train.txt']
	valid_datasets_m = [base_path + '/data/word_sequence/premise_multinli_1.0_dev_matched.txt',
					  base_path + '/data/word_sequence/hypothesis_multinli_1.0_dev_matched.txt',
					  base_path + '/data/word_sequence/label_multinli_1.0_dev_matched.txt']
	valid_datasets_um = [base_path + '/data/word_sequence/premise_multinli_1.0_dev_mismatched.txt',
						base_path + '/data/word_sequence/hypothesis_multinli_1.0_dev_mismatched.txt',
						base_path + '/data/word_sequence/label_multinli_1.0_dev_mismatched.txt']
	test_datasets_m = [base_path + '/data/word_sequence/premise_multinli_1.0_test_matched.txt',
					  base_path + '/data/word_sequence/hypothesis_multinli_1.0_test_matched.txt',
					  base_path + '/data/word_sequence/label_multinli_1.0_test_matched.txt']
	test_datasets_um = [base_path + '/data/word_sequence/premise_multinli_1.0_test_mismatched.txt',
						base_path + '/data/word_sequence/hypothesis_multinli_1.0_test_mismatched.txt',
						base_path + '/data/word_sequence/label_multinli_1.0_test_mismatched.txt']
elif task=='trecqa':
	if torch.cuda.is_available():
		print('CUDA is available!')
		base_path = expanduser("~") + '/pytorch/DeepPairWiseWord/data/trecqa'
		embedding_path = expanduser("~") + '/pytorch/DeepPairWiseWord/VDPWI-NN-Torch/data/glove'
		castorini_path = expanduser("~") + '/pytorch/DeepPairWiseWord/data/castorini/trec_eval.9.0/trec_eval'
	else:
		base_path = expanduser("~") + '/Documents/research/pytorch/DeepPairWiseWord/data/trecqa'
		embedding_path = expanduser("~") + '/Documents/research/pytorch/DeepPairWiseWord/VDPWI-NN-Torch/data/glove'
		castorini_path = expanduser("~") + '/Documents/research/pytorch/DeepPairWiseWord/data/castorini/trec_eval.9.0/trec_eval'
	dictionary=base_path+'/trecqa_vocab_cased.pkl'
	datasets=[base_path+'/train/a.toks', base_path+'/train/b.toks', base_path+'/train/sim.txt']
	test_datasets=[base_path+'/test/a.toks', base_path+'/test/b.toks', base_path+'/test/sim.txt']

cmd = ('%s -m map %s %s' % (castorini_path, base_path + '/test.qrel', base_path + '/result_ESIM_' + task))
os.system(cmd)
cmd = ('%s -m recip_rank %s %s' % (castorini_path, base_path + '/test.qrel', base_path + '/result_ESIM_' + task))
os.system(cmd)

#n_words=42394
dim_word=300
batch_size=32
num_epochs=500
valid_batch_size=32
print 'Loading data'
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
train = TextIterator(datasets[0], datasets[1], datasets[2],
					 dictionary,
					 n_words=n_words,
					 batch_size=batch_size)
test = TextIterator(test_datasets[0], test_datasets[1], test_datasets[2],
					 dictionary,
					 n_words=n_words,
					 batch_size=valid_batch_size,
					 shuffle=False)

criterion = torch.nn.CrossEntropyLoss()
model = ESIM(dim_word, 2, n_words, dim_word, pretrained_emb)
if torch.cuda.is_available():
	model = model.cuda()
	criterion = criterion.cuda()
optimizer = torch.optim.Adam(model.parameters(),lr=0.0004)
print('start training...')
accumulated_loss=0
batch_counter=0
report_interval = 1000
best_dev_loss=10e10
best_dev_loss2=10e10
clip_c=10
max_len=100
max_result=0
best_result = 0

model.train()
for epoch in range(num_epochs):
	accumulated_loss = 0
	model.train()
	print('--' * 20)
	start_time = time.time()
	train_sents_scaned = 0
	train_num_correct = 0
	batch_counter=0
	for x1, x2, y in train:
		x1, x1_mask, x2, x2_mask, y = prepare_data(x1, x2, y, maxlen=max_len)
		train_sents_scaned += len(y)
		optimizer.zero_grad()
		output = model(x1, x1_mask, x2, x2_mask)
		result = output.data.cpu().numpy()
		a = np.argmax(result, axis=1)
		b = y.data.cpu().numpy()
		train_num_correct += np.sum(a == b)
		loss = criterion(output, y)
		loss.backward()

		''''''
		grad_norm = 0.

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
		if batch_counter % report_interval == 0:
			msg = '%d completed epochs, %d batches' % (epoch, batch_counter)
			msg += '\t training batch loss: %f' % (accumulated_loss / train_sents_scaned)
			#msg += '\t train accuracy: %f' % (train_num_correct / train_sents_scaned)
			print(msg)
	# test after each epoch
	model.eval()
	msg = '%d completed epochs, %d batches' % (epoch, batch_counter)
	accumulated_loss = 0
	dev_num_correct = 0
	n_done = 0
	pred=[]
	gold = []
	for test_x1, test_x2, test_y in test:
		n_done+=len(test_y)
		x1, x1_mask, x2, x2_mask, y = prepare_data(test_x1, test_x2, test_y, maxlen=max_len)
		with torch.no_grad():
			output = F.softmax(model(x1, x1_mask, x2, x2_mask))
		result = output.data.cpu().numpy()
		loss = criterion(output, y)
		accumulated_loss += loss.data[0]
		a = numpy.argmax(result, axis=1)
		b = y.data.cpu().numpy()
		dev_num_correct += numpy.sum(a == b)
		pred.extend(result[:, 1])
		gold.extend(b)
	msg += '\t test loss: %f' % (accumulated_loss / n_done)
	test_acc = dev_num_correct / n_done
	#msg += '\t test accuracy: %f' % test_acc
	print(msg)
	_, my_result = URL_maxF1_eval(pred, gold)
	if my_result > best_result:
		best_result=my_result
		torch.save(model, base_path + '/model_ESIM_batch_' + task + '.pkl')
		with open(base_path+'/result_ESIM_batch_'+task+'_prob.txt','w') as f:
			for i in range(len(pred)):
				f.writelines(str(1 - pred[i]) + '\t' + str(pred[i]) + '\n')
		if task == 'wikiqa' or task == 'trecqa':
			list1 = []
			for line in open(base_path + '/test.qrel'):
				list1.append(line.strip().split())
			with open(base_path + '/result_ESIM_' + task, 'w') as f:
				for i in range(len(pred)):
					f.writelines(str(list1[i][0]) + '\t' + str(list1[i][1]) + '\t' + str(
						list1[i][2]) + '\t' + '*\t' + str(pred[i]) + '\t' + '*\n')
			cmd = ('%s -m map %s %s' % (castorini_path, base_path + '/test.qrel', base_path + '/result_ESIM_' + task))
			os.system(cmd)
			cmd = ('%s -m recip_rank %s %s' % (castorini_path, base_path + '/test.qrel', base_path + '/result_ESIM_' + task))
			os.system(cmd)
	elapsed_time = time.time() - start_time
	print('Epoch ' + str(epoch) + ' finished within ' + str(timedelta(seconds=elapsed_time)))