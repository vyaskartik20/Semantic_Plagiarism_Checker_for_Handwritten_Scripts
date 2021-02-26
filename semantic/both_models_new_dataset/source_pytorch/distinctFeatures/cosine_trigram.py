
from __future__ import division
import numpy as np
from sklearn.metrics import jaccard_score
from math import log10, sqrt
from string import punctuation
import os
import nltk

# Variables
MODEL = 'trigram'
MEASURE = 'cosine'
NUM_DOCS = 0
MASTER_DOC = 'combined_docs'
STOPWORDS = 'nltk_en_stopwords'
DATASET = 'docs'

# Return unigram unique words from a text
def extract_unique_words(text):
	#return text.translate(None, punctuation).split()
	return set(text.translate(punctuation).lower().split())


# Return bigram unique words from a text
def extract_bigram_unique_words(text):
	# Remove punctuations
	text_no_punctuations = text.translate(punctuation).lower().split()

	# Create bigrams from the input text
	bigrms = list(nltk.bigrams(text_no_punctuations))

	# Create unique bigrams
	unique_bigrms = set(bigrms)

	# Convert the set of unique bigrams back into list
	list_of_unique_bigrms = list(unique_bigrms)

	# Create list of unique bigrams represented as string
	list_of_unique_bigrms_str = [ "%s %s" % x for x in list_of_unique_bigrms ]

	return list_of_unique_bigrms_str


# Return trigram unique words from a text
def extract_trigram_unique_words(text):
	# Remove punctuations
	text_no_punctuations = text.translate(punctuation).lower().split()

	# Create trigrams from the input text
	trigrms = list(nltk.trigrams(text_no_punctuations))

	# Create unique trigrams
	unique_trigrms = set(trigrms)

	# Convert the set of unique trigrams back into list
	list_of_unique_trigrms = list(unique_trigrms)

	# Create list of unique trigrams represented as string
	list_of_unique_trigrms_str = [ "%s %s %s" % x for x in list_of_unique_trigrms ]

	return list_of_unique_trigrms_str


# Return the document frequency for each term in the input list
def computeDFs(unique_words, list_of_assignment_files):
	# DF for each term t (dfT) was calculated by counting the number of
	# documents which had the term t
	list_of_df = []

	for unique_word in unique_words:
		counter = 0
		for assignment_file in list_of_assignment_files:
			with open(assignment_file, 'r') as f:
				all_text = f.read().replace('\n', ' ')

			
			# Convert the whole text into lower case
			all_text = all_text.lower()

			# Replace single quote (" ' ") into single white space
			all_text_no_quote = all_text.replace("'", " ")


			if unique_word in all_text_no_quote:
				counter = counter + 1

		list_of_df.append(counter)

	return list_of_df

# Return the inverse document frequency for each term in the input list
def computeIDFs(NUM_DOCS, DFs):
	# Formula: idf(t) = 1 + log N / df(t)
	# df(t) = document frequency for term t
	# idf(t) = inverse document frequency for term t
	# N = total number of documents
	list_of_idf = []

	for df in DFs:
		idf = 0

		if df == 0:
			idf = 1
		else:
			idf = 1 + (log10(NUM_DOCS / df))

		list_of_idf.append(idf)

	return list_of_idf


# Return the term frequency of a term in a document
def computeTF(assignment_file, unique_word):
	# with open(assignment_file, 'r') as f:
	all_text = assignment_file.replace('\n', ' ')

	# Convert the whole text into lower case
	all_text = all_text.lower()

	# Replace single quote (" ' ") into single white space
	all_text_no_quote = all_text.replace("'", " ")

	return all_text_no_quote.count(unique_word) / computeNumOfWordsInText(all_text_no_quote)


# Return the TF-IDF weight vector for a document
def computeTFIDFweightvector(assignment_file, unique_words, IDFs):
	# Wtd = TFtd x IDFt
	# Wtd = TF-IDF weight vector
	# TFtd = frequency of a term in a document
	# IDFt = inverse document frequency for term t
	list_of_TFIDFweightvector = []

	for idx in range(0, len(unique_words)):
		TF = computeTF(assignment_file, unique_words[idx])

		# print ('TF')
		# print (TF)
		# print ('\n')

		weightVector = TF * IDFs[idx]

		# print ('Weight Vector')
		# print (weightVector)
		# print ('\n')
		
		list_of_TFIDFweightvector.append(weightVector)

	return list_of_TFIDFweightvector


# Return the value of cosine between two document vectors
def compareDocument(TFIDF_weightvector_1, TFIDF_weightvector_2):
	# Compute the dot products
	dotProducts = 0
	
	for idx in range(0, len(TFIDF_weightvector_1)):
		dotProducts = dotProducts + (TFIDF_weightvector_1[idx] * TFIDF_weightvector_2[idx])

	# Compute the magnitude of the 1st TFIDF weight vector
	magnitude_1 = 0
	for idx in range(0, len(TFIDF_weightvector_1)):
		magnitude_1 = magnitude_1 + (TFIDF_weightvector_1[idx] * TFIDF_weightvector_1[idx])

	# Compute the magnitude of the 2nd TFIDF weight vector
	magnitude_2 = 0
	for idx in range(0, len(TFIDF_weightvector_2)):
		magnitude_2 = magnitude_2 + (TFIDF_weightvector_2[idx] * TFIDF_weightvector_2[idx])

	# Compute the cosine
	if magnitude_1 == 0:
		magnitude_1 = 0.000001
	if magnitude_2 == 0:
		magnitude_2 = 0.000001
  
	# print( str((dotProducts)) + ' 		' + str((magnitude_2)) + 
    #    ' 		' +  str((magnitude_2)))

	cosine = dotProducts / (sqrt(magnitude_1) * sqrt(magnitude_2))

	return cosine


# Return the value of jaccard similarity between two document vectors
def compareDocumentJaccard(TFIDF_weightvector_1, TFIDF_weightvector_2):

	# How to read the Jaccard coeficient:
	# The coeficient is multiplied by 100
	# Two sets that share all members would be 100% similar
	# The closer to 100%, the more similarity (e.g. 90% is more similar than 89%)
	# If they share no members, they are 0% similar
	# The midway point (50%) means that the two sets share half of the members


	# Find the intersection between two document vectors
	TFIDF_weightvector_intersection = []
	
	for tfidfweightvector_1 in TFIDF_weightvector_1:
		if tfidfweightvector_1 in TFIDF_weightvector_2:
			TFIDF_weightvector_intersection.append(tfidfweightvector_1)
			break

	# Find the union of all elements (unique values) from both document vectors
	TFIDF_weightvector_union = []

	for tfidfweightvector_1 in TFIDF_weightvector_1:
		TFIDF_weightvector_union.append(tfidfweightvector_1)

	for tfidfweightvector_2 in TFIDF_weightvector_2:
		TFIDF_weightvector_union.append(tfidfweightvector_2)

	TFIDF_weightvector_union = list(set(TFIDF_weightvector_union))


	# Compute the Jaccard coeficient

	# print( str(len(TFIDF_weightvector_intersection)) + ' 		' + str(len(TFIDF_weightvector_union)) + 
    #    ' 		' +  str(len(TFIDF_weightvector_1)) + ' 		' + str(len(TFIDF_weightvector_2)) + ' 		' )
 
	jaccardCoef = len(TFIDF_weightvector_intersection) / len(TFIDF_weightvector_1)

	return jaccardCoef


# Return the list of unique words without stopwords
def eliminateStopwords(unique_words):
	stopwords = nltk.corpus.stopwords.words('english')

	no_stopwords_list = []

	for unique_word in unique_words:
		words = unique_word.split()

		no_stopwords_list.append(unique_word)

		for word in words:
			if word in stopwords:
				no_stopwords_list.pop()
				break

	return no_stopwords_list


# Return the number of unigram words in a string
def computeNumOfWordsInText(text):
	numOfWords = len(text.split())
	# print ('WORDS : 		' +  str(numOfWords))

	if MODEL == 'bigram':
		if numOfWords == 1:
			numOfWords = 0
		else:
			numOfWords = numOfWords - 1
	elif MODEL == 'trigram':
		if numOfWords == 1 or numOfWords == 2:
			numOfWords = 0
		else:
			numOfWords = numOfWords - 2

	return numOfWords


# Combine all documents into one file called MASTER DOCUMENT
def similarity(text1,text2):
	assignment_files = []

	data = ""
	data2 = ""

	data = text1
	data = data + "\n"
	data = data + text2

	# for fname in assignment_files :
	# 	data2= open(fname).read()
	# 	data = data + data2
	# 	data = data + "\n"

	file2=open(MASTER_DOC,"w")
	file2.write(data)
	file2.close()

	# with open(MASTER_DOC, 'w') as outfile:
	# 	for fname in assignment_files:
	# 		with open(fname) as infile:
	# 			for line in infile:
	# 				outfile.write(line)

	# Extract unique words (unigram, bigram, trigram) from the MASTER DOCUMENT
	with open(MASTER_DOC, 'r') as f:
		all_text = f.read().replace('\n', ' ')


	# Convert the whole text into lower case
	all_text = all_text.lower()

	# Replace single quote (" ' ") into single white space
	all_text_no_quote = all_text.replace("'", " ")

	# Create unique words (vocabulary) based on the applied model
	# Default is unigram
	unique_words = extract_unique_words(all_text_no_quote)

	if MODEL == 'bigram':
		# Unique words for bigram vector
		unique_words = extract_bigram_unique_words(all_text_no_quote)
	elif MODEL == 'trigram':
		# Unique words for trigram vector
		unique_words = extract_trigram_unique_words(all_text_no_quote)



	# DATASET PREPROCESSING

	# Eliminate stopwords
	'''
	with open(STOPWORDS, 'r') as f:
		stopwords = f.readlines()

	stopwords = [x.strip() for x in stopwords]

	unique_words_no_stopwords = [x for x in unique_words if x not in stopwords]
	'''

	unique_words_no_stopwords = eliminateStopwords(unique_words)

	# print ('Unique words without stopwords')
	# print(len(unique_words))
	# print(len(unique_words_no_stopwords))
	# print (unique_words_no_stopwords)



	# VECTOR SPACE MODEL WITH COSINE SIMILARITY MEASURE

	# NUM_DOCS = len(assignment_files)

	# Computer Document Frequency (DF) for each term t
	DFs = computeDFs(unique_words_no_stopwords, assignment_files)

	# print ('DFs')
	# print (DFs)
	# print ('\n')

	# Compute Inverse Document Frequency (IDF) for each term t
	IDFs = computeIDFs(2, DFs)

	# print ('IDFs')
	# print (IDFs)
	# print ('\n')

	# Compute TF-IDF weight vector for each document
	TFIDF_weightvectors = []
	numOfWords = []


	TFIDF_weightvectors.append(computeTFIDFweightvector(text1, unique_words_no_stopwords, IDFs))
	# with open(assignment_file, 'r') as f:
	all_text = text1.replace('\n', ' ')

	# Convert the whole text into lower case
	all_text = all_text.lower()

	# Replace single quote (" ' ") into single white space
	all_text_no_quote = all_text.replace("'", " ")
	tempNumOfWords = len(all_text_no_quote.split())
	numOfWords.append(tempNumOfWords)
 
 
	TFIDF_weightvectors.append(computeTFIDFweightvector(text2, unique_words_no_stopwords, IDFs))
	# with open(assignment_file, 'r') as f:
	all_text = text2.replace('\n', ' ')

	# Convert the whole text into lower case
	all_text = all_text.lower()

	# Replace single quote (" ' ") into single white space
	all_text_no_quote = all_text.replace("'", " ")
	tempNumOfWords = len(all_text_no_quote.split())
	numOfWords.append(tempNumOfWords)

	# print ('TFIDF weight vectors')
	# print (TFIDF_weightvectors)
	# print ('\n')



	if MEASURE == 'cosine':
		# Compare each pair of assignment using Cosine Similarity
		
		cosineSim = compareDocument(TFIDF_weightvectors[0], TFIDF_weightvectors[0])
		cosineSim = cosineSim * (numOfWords[0] + numOfWords[1] ) / (2*numOfWords[0]) 
		if(cosineSim>1):
			cosineSim=1
		# print ('Cosine similarity measure of document {0} from {1} gives {2} as the result'.format(0, 1, cosineSim))
		return cosineSim
	else:
		# Compare each pair of assignment using Jaccard Similarity
		
		jaccardSim = compareDocumentJaccard(TFIDF_weightvectors[0], TFIDF_weightvectors[1])
		jaccardSim = jaccardSim * (numOfWords[0] + numOfWords[1] ) / (2*numOfWords[0]) 
		# print ('Jaccard similarity measure of document {0} from {1} gives {2} as the result'.format(0, 1, jaccardSim))
		return jaccardSim

def create_cosine_trigram_features(df):
    cosine_trigram_values = []

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
            try :   
            	value = similarity(answer_text,source_text)
            except :
                value =0
            if value >1: 
                value = 1
            if value < 0:
                value = 0
            cosine_trigram_values.append(value)
        else:
            cosine_trigram_values.append(-1)

    print('cosine_trigram features created!')
    return cosine_trigram_values


# f = open('data1.txt', encoding="utf8")
# file1_data = f.read()
# # print (similarity.returnTable(similarity.report(str(file1_data))))
# text1 = (str(file1_data))

# f = open('data2.txt', encoding="utf8")
# file2_data = f.read()
# # print (similarity.returnTable(similarity.report(str(file1_data))))
# text2 = (str(file2_data))

# text1 = "two dogs are wrestling and hugging"
# text2 = "two dogs are fighting"

# value = similarity(text1,text2)
# print(value)