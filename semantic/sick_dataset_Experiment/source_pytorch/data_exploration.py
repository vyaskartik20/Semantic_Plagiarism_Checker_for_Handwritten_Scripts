# import os

# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd

# csv_file = 'data/file_information.csv'
# plagiarism_df = pd.read_csv(csv_file)

# # print out the first few rows of data info
# print(plagiarism_df.head(10))

# # print out some stats about the data
# print('Number of files: ', plagiarism_df.shape[0])  # .shape[0] gives the rows 
# # .unique() gives unique items in a specified column
# print('Number of unique tasks/question types (A-E): ', (len(plagiarism_df['Task'].unique())))
# print('Unique plagiarism categories: ', (plagiarism_df['Category'].unique()))


# # Show counts by different tasks and amounts of plagiarism

# # group and count by task
# counts_per_task=plagiarism_df.groupby(['Task']).size().reset_index(name="Counts")
# print("\nTask:")
# print(counts_per_task)

# # group by plagiarism level
# counts_per_category=plagiarism_df.groupby(['Category']).size().reset_index(name="Counts")
# print("\nPlagiarism Levels:")
# print(counts_per_category)

# # group by task AND plagiarism level
# counts_task_and_plagiarism=plagiarism_df.groupby(['Task', 'Category']).size().reset_index(name="Counts")
# print("\nTask & Plagiarism Level Combos :")
# print(counts_task_and_plagiarism)

# # counts
# group = ['Task', 'Category']
# counts = plagiarism_df.groupby(group).size().reset_index(name="Counts")

# plt.figure(figsize=(8,5))
# plt.bar(range(len(counts)), counts['Counts'], color = 'blue')
# plt.show()



# Calculate the ngram containment for one answer file/source file pair in a df
def calculate_containment(df, n, answer_filename):
    """
    Calculates the containment between a given answer text and its associated source text.
    This function creates a count of ngrams (of a size, n) for each text file in our data.
    Then calculates the containment by finding the ngram count for a given answer text, 
    and its associated source text, and calculating the normalized intersection of those counts.
    
    Arguments
    :param df: A dataframe with columns,
        'File', 'Task', 'Category', 'Class', 'Text', and 'Datatype'
    :param n: An integer that defines the ngram size
    :param answer_filename: A filename for an answer text in the df, ex. 'g0pB_taskd.txt'
    
    Return
    :return: A single containment value that represents the similarity
        between an answer text and its source text.
    """
    
    answer_df = df.query('File == @answer_filename')
    a_text = answer_df.iloc[0].at['Text']
    source_filename = 'source'+answer_filename[6]+'.txt'
    source_df = df.query('File == @source_filename')
    s_text = source_df.iloc[0].at['Text']

    counts = CountVectorizer(analyzer='word', ngram_range=(n,n))
    ngrams = counts.fit_transform([a_text, s_text])
    ngram_array = ngrams.toarray()

    intersection = [min(a, s) for a, s in zip(*ngram_array)]
    c_value = sum(intersection) / sum(ngram_array[0])

    return c_value





import pandas as pd
import helpers
import plagiarism_feature_engineering
import numpy as np
# import distinctFeatures/cosine_1
# from distinctFeatures import cosine_1
# from distinctFeatures import cosine_2
# from distinctFeatures import cosine_trigram
# from distinctFeatures import docism_nltk
# from distinctFeatures import jaccard_trigram
# from distinctFeatures import lcs
# from distinctFeatures import ngram
# from distinctFeatures import phrase_nltk_1
# from distinctFeatures import phrase_nltk_2
# # from distinctFeatures import rabin_karp_1
# from distinctFeatures import rabin_karp_2
# from distinctFeatures import sequence_matcher
# from distinctFeatures import embed_spacy
from distinctFeatures import bert_sentence_encoder


csv_file = 'data/file_information.csv'
complete_df = pd.read_csv(csv_file)

# text_df = helpers.create_text_column(complete_df)


# check work
# print('\nExample data: ')
# print(text_df.head(10))

# sample_text = text_df.iloc[0]['Text']

# print('Sample processed text:\n\n', sample_text)

# # complete_df = helpers.train_test_dataframe(text_df, random_seed=1)

# text_df.to_csv('data/file_information.csv') 

# print('\nExample data: ')

# print(complete_df.head(100))

# i=1
# count = 0
# while i <  1000  :
#     sample_text1 = complete_df.iloc[i]['File']
#     sample_text2 = complete_df.iloc[i]['Datatype']
#     i=i+2
#     if(sample_text2 == "test"):
#         count = count+ 1
#     # print( sample_text1, sample_text2)
    
# print (f"test files : {count } ")
# print (f"train files : {500-count} ")

# n = 5

# # indices for first few files
# test_indices = range(400)

# # iterate through files and calculate containment
# class_vals = []
# containment_vals = []
# for i in test_indices:
#     # get level of plagiarism for a given file index
#     class_vals.append(complete_df.loc[i, 'Class'])
#     # calculate containment for given file and n
#     filename = complete_df.loc[i, 'File']
#     c = plagiarism_feature_engineering.calculate_containment(complete_df, n, filename)
#     containment_vals.append(c)

# print out result, does it make sense?
# print('Original category values: \n', class_vals)
# print()
# print(str(n)+'-gram containment values: \n', containment_vals)

# for i in range(0,400,1) :
#     if class_vals[i] != -1 :
#         print( str(class_vals[i]) + "   :::   " + str(containment_vals[i]))
        
        

        
        
ngram_range = [1,2,3,4]


# The following code may take a minute to run, depending on your ngram_range
"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
features_list = []

# Create features in a features_df
all_features = np.zeros((1, len(complete_df)))

i=0

features_list.append("bert_sentence_encoder")
all_features[i]= np.squeeze(bert_sentence_encoder.create_bert_sentence_encoder_features(complete_df))

# from distinctFeatures import tensorflow_sentence_embedding
# features_list.append("tensorflow_sentence_embedding")
# all_features[i]= np.squeeze(tensorflow_sentence_embedding.create_tensorflow_sentence_embedding_features(complete_df))
# i+=1

# features_list.append("embed_spacy")
# all_features[i]= np.squeeze(embed_spacy.create_embed_spacy_features(complete_df))
# i+=1

# for n in ngram_range:
#     column_name = 'c_'+str(n)
#     features_list.append(column_name)
#     # create containment features
#     all_features[i]=np.squeeze(ngram.create_containment_features(complete_df, n))
#     print(f"n gram  :::     {n}")
#     i+=1

# features_list.append("docism_nltk")
# all_features[i]= np.squeeze(docism_nltk.create_docism_nltk_features(complete_df))
# i+=1

# features_list.append("cosine_trigram")
# all_features[i]= np.squeeze(cosine_trigram.create_cosine_trigram_features(complete_df))
# i+=1



# features_list.append("cosine_1")
# all_features[i]= np.squeeze(cosine_1.create_cosine_1_features(complete_df))
# i+=1

# features_list.append("cosine_2")
# all_features[i]= np.squeeze(cosine_2.create_cosine_2_features(complete_df))
# i+=1



# features_list.append("jaccard_trigram")
# all_features[i]= np.squeeze(jaccard_trigram.create_jaccard_trigram_features(complete_df))
# i+=1

# # Calculate features for LCS_Norm Words 
# features_list.append('lcs_word')
# all_features[i]= np.squeeze(lcs.create_lcs_features(complete_df))
# i+=1


# features_list.append("rabin_karp_2")
# all_features[i]= np.squeeze(rabin_karp_2.create_rabin_karp_2_features(complete_df))
# i+=1


# features_list.append("sequence_matcher")
# all_features[i]= np.squeeze(sequence_matcher.create_sequence_matcher_features(complete_df))


# create a features dataframe
features_df = pd.DataFrame(np.transpose(all_features), columns=features_list)

# # Calculate features for containment for ngrams in range

# features_list.append("rabin_karp_1")
# all_features[i]= np.squeeze(rabin_karp_1.create_rabin_karp_1_features(complete_df))
# i+=1

# features_list.append("phrase_nltk_1")
# all_features[i]= np.squeeze(phrase_nltk_1.create_phrase_nltk_1_features(complete_df))
# i+=1

# features_list.append("phrase_nltk_2")
# all_features[i]= np.squeeze(phrase_nltk_2.create_phrase_nltk_2_features(complete_df))
# i+=1

# Print all features/columns
# print()
# print('Features: ', features_list)
# print()

test_selection = list(features_df)[:1] # first couple columns as a test
(train_x, train_y), (test_x, test_y) = plagiarism_feature_engineering.train_test_data(complete_df, features_df, test_selection)

data_dir = 'plagiarism_data'

plagiarism_feature_engineering.make_csv(train_x, train_y, filename='train.csv', data_dir=data_dir)
plagiarism_feature_engineering.make_csv(test_x, test_y, filename='test.csv', data_dir=data_dir)