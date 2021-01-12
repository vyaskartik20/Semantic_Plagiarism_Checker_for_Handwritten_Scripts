
# import libraries
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

import helpers
import problem_unittests as tests

# csv_file = 'data/file_information.csv'
# plagiarism_df = pd.read_csv(csv_file)

# # print out the first few rows of data info
# plagiarism_df.head()


# # Dict mapping category names to category value and class
# cat_dict = {'non': (0, 0),
#             'heavy': (1, 1),
#             'light': (2, 1),
#             'cut': (3, 1),
#             'orig': (-1, -1)}

# def convert_to_numerical(row):
#     """
#     Convert the Category column from string to numerical values.
#     Create a new column labeling plagiarism
    
#     Arguments
#     :param row: one row of a dataframe
#     """
#     cat_value, cat_class = cat_dict[row['Category']]
#     row['Category'] = cat_value
#     row['Class'] = cat_class
#     return row

# # Read in a csv file and return a transformed dataframe
# def numerical_dataframe(csv_file='data/file_information.csv'):
#     """
#     Reads in a csv file which is assumed to have `File`, `Category` and `Task` columns.
#     This function does two things:
#     1) converts `Category` column values to numerical values
#     2) Adds a new, numerical `Class` label column.
#     The `Class` column will label plagiarized answers as 1 and non-plagiarized as 0.
#     Source texts have a special label, -1.
    
#     Arguments:
#     :param csv_file: The directory for the file_information.csv file
    
#     Return:
#     :return: A dataframe with numerical categories and a new `Class` label column
#     """
#     df = pd.read_csv(csv_file)
#     df = df.apply(convert_to_numerical, axis=1)
#     return df

# # informal testing, print out the results of a called function
# # create new `transformed_df`
# transformed_df = numerical_dataframe(csv_file ='data/file_information.csv')

# # check work
# # check that all categories of plagiarism have a class label = 1
# #print(transformed_df.head(10))

# """
# DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
# """
# # create a text column 
# text_df = helpers.create_text_column(transformed_df)
# text_df.head()


# # after running the cell above
# # check out the processed text for a single file, by row index
# row_idx = 0 # feel free to change this index

# sample_text = text_df.iloc[0]['Text']

# #print('Sample processed text:\n\n', sample_text)

# random_seed = 1 # can change; set for reproducibility

# """
# DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
# """
# # create new df with Datatype (train, test, orig) column
# # pass in `text_df` from above to create a complete dataframe, with all the information you need
# complete_df = helpers.train_test_dataframe(text_df, random_seed=random_seed)

# # check results
# #print(complete_df.tail(10))


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
    # source_filename = answer_filename
    # source_filename[0]="s"
    # source_filename[1]="o"
    # source_filename[2]="u"
    # source_filename[3]="r"
    # source_filename[4]="c"
    # source_filename[5]="e"
    source_filename = "source" + answer_filename[6:]
    source_df = df.query('File == @source_filename')
    s_text = source_df.iloc[0].at['Text']

    counts = CountVectorizer(analyzer='word', ngram_range=(n,n))
    ngrams = counts.fit_transform([a_text, s_text])
    ngram_array = ngrams.toarray()

    intersection = [min(a, s) for a, s in zip(*ngram_array)]
    c_value = sum(intersection) / sum(ngram_array[0])

    return c_value

# select a value for n
# n = 3

# # indices for first few files
# test_indices = range(5)

# # iterate through files and calculate containment
# category_vals = []
# containment_vals = []
# for i in test_indices:
#     # get level of plagiarism for a given file index
#     category_vals.append(complete_df.loc[i, 'Category'])
#     # calculate containment for given file and n
#     filename = complete_df.loc[i, 'File']
#     c = calculate_containment(complete_df, n, filename)
#     containment_vals.append(c)

# # print out result, does it make sense?
# print('Original category values: \n', category_vals)
# print()
# print(str(n)+'-gram containment values: \n', containment_vals)

# Compute the normalized LCS given an answer text and a source text
def lcs_norm_word(answer_text, source_text):
    """
    Computes the longest common subsequence of words in two texts;
    returns a normalized value.
    
    Arguments:
    :param answer_text: The pre-processed text for an answer text
    :param source_text: The pre-processed text for an answer's associated source text
    
    Return:
    :return: A normalized LCS value
    """

    answer_words = answer_text.split()
    answer_len = len(answer_words)
    source_words = source_text.split()
    source_len = len(source_words)

    lcs_matrix = np.zeros(shape=(source_len+1,answer_len+1), dtype='int')

    for i, s in enumerate(source_words, 1):
        for j, a in enumerate(answer_words, 1):
            if a == s:
                lcs_matrix[i,j] = lcs_matrix[i-1,j-1] + 1
            else:
                lcs_matrix[i,j] = max(lcs_matrix[i,j-1], lcs_matrix[i-1,j])

    return lcs_matrix[source_len][answer_len] / answer_len

# Run the test scenario from above
# does your function return the expected value?

# A = "i think pagerank is a link analysis algorithm used by google that uses a system of weights attached to each element of a hyperlinked set of documents"
# S = "pagerank is a link analysis algorithm used by the google internet search engine that assigns a numerical weighting to each element of a hyperlinked set of documents"

# # calculate LCS
# lcs = lcs_norm_word(A, S)
# #print('LCS = ', lcs)


# # expected value test
# assert lcs==20/27., "Incorrect LCS value, expected about 0.7408, got "+str(lcs)

# #print('Test passed!')


"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
# Function returns a list of containment features, calculated for a given n 
# Should return a list of length 100 for all files in a complete_df
def create_containment_features(df, n, column_name=None):
    
    containment_values = []
    
    if(column_name==None):
        column_name = 'c_'+str(n) # c_1, c_2, .. c_n
    
    # iterates through dataframe rows
    for i in df.index:
        file = df.loc[i, 'File']
        # Computes features using calculate_containment function
        if df.loc[i,'Class'] > -1:
            c = calculate_containment(df, n, file)
            containment_values.append(c)
        # Sets value to -1 for original tasks 
        else:
            containment_values.append(-1)
    
    print(str(n)+'-gram containment features created!')
    return containment_values


"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
# Function creates lcs feature and add it to the dataframe
def create_lcs_features(df, column_name='lcs_word'):
    
    lcs_values = []
    
    # iterate through files in dataframe
    for i in df.index:
        # Computes LCS_norm words feature using function above for answer tasks
        if df.loc[i,'Class'] > -1:
            # get texts to compare
            answer_text = df.loc[i, 'Text']
            answer_filename = df.loc[i, 'File'] 
            # task = df.loc[i, 'Task']
            # we know that source texts have Class = -1
            # orig_rows = df[(df['Class'] == -1)]
            # orig_row = orig_rows[(orig_rows['Task'] == task)]
            # source_text = orig_row['Text'].values[0]
            source_filename = answer_filename
            # source_filename[0]='s'
            # source_filename[1]='o'
            # source_filename[2]='u'
            # source_filename[3]='r'
            # source_filename[4]='c'
            # source_filename[5]='e'
            source_filename = "source" + answer_filename[6:]     
            source_df = df.query('File == @source_filename')
            source_text = source_df.iloc[0].at['Text']

            # calculate lcs
            lcs = lcs_norm_word(answer_text, source_text)
            lcs_values.append(lcs)
        # Sets to -1 for original tasks 
        else:
            lcs_values.append(-1)

    print('LCS features created!')
    return lcs_values


# Define an ngram range
# ngram_range = range(1,11)


# # The following code may take a minute to run, depending on your ngram_range
# """
# DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
# """
# features_list = []

# # Create features in a features_df
# all_features = np.zeros((len(ngram_range)+1, len(complete_df)))

# # Calculate features for containment for ngrams in range
# i=0
# for n in ngram_range:
#     column_name = 'c_'+str(n)
#     features_list.append(column_name)
#     # create containment features
#     all_features[i]=np.squeeze(create_containment_features(complete_df, n))
#     i+=1

# # Calculate features for LCS_Norm Words 
# features_list.append('lcs_word')
# all_features[i]= np.squeeze(create_lcs_features(complete_df))

# # create a features dataframe
# features_df = pd.DataFrame(np.transpose(all_features), columns=features_list)

# Print all features/columns
#print()
#print('Features: ', features_list)
#print()


# print some results 
#print(features_df.head(10))

"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
# Create correlation matrix for just Features to determine different models to test
# corr_matrix = features_df.corr().abs().round(2)

# # display shows all of a dataframe
# print((corr_matrix))

# for i in range(corr_matrix.shape[0]):
#     corr_matrix.iloc[i, i] = np.nan

# print('\nCorrelation Matrix description:')
# print(corr_matrix.describe())

# print('\nCorrelation Matrix boxplot:')
# corr_matrix.plot.box()
# plt.show()


# Takes in dataframes and a list of selected features (column names) 
# and returns (train_x, train_y), (test_x, test_y)
def train_test_data(complete_df, features_df, selected_features):
    """
    Gets selected training and test features from given dataframes, and 
    returns tuples for training and test features and their corresponding class labels.
    
    Arguments:
    :param complete_df: A dataframe with all of our processed text data, datatypes, and labels
    :param features_df: A dataframe of all computed, similarity features
    :param selected_features: An array of selected features that correspond to certain columns in `features_df`
    
    Return:
    :return: training and test features and labels: (train_x, train_y), (test_x, test_y)
    """

    train_test_df = complete_df.join(features_df[selected_features])
    train_df = train_test_df.query('Datatype == "train"')
    test_df = train_test_df.query('Datatype == "test"')
    
    # get the training features
    train_x = train_df[selected_features]
    # And training class labels (0 or 1)
    train_y = train_df['Class']

    # get the test features and labels
    test_x = test_df[selected_features]
    test_y = test_df['Class']

    return (train_x.values, train_y.values), (test_x.values, test_y.values)

# Select your list of features, this should be column names from features_df
# ex. ['c_1', 'lcs_word']
# selected_features = ['lcs_word', 'c_10', 'c_1']


"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""

# (train_x, train_y), (test_x, test_y) = train_test_data(complete_df, features_df, selected_features)

# check that division of samples seems correct
# these should add up to 95 (100 - 5 original files)
# print('Training size: ', len(train_x))
# print('Test size: ', len(test_x))
# print()
# print('Training df sample: \n', train_x[:10])

def make_csv(x, y, filename, data_dir):
    """
    Merges features and labels and converts them into one csv file with labels in the first column.
    
    Arguments:
    :param x: Data features
    :param y: Data labels
    :param file_name: Name of csv file, ex. 'train.csv'
    :param data_dir: The directory where files will be saved
    """

    # make data dir, if it does not exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    file_path = str(data_dir)+'/'+str(filename)

    df = pd.DataFrame([(label, *cols) for (label, cols) in zip(y, x)])
    df.dropna(axis=0)

    df.to_csv(file_path, header=False, index=False)

    # nothing is returned, but a print statement indicates that the function has run
    print('Path created: '+file_path)


# can change directory, if you want
# data_dir = 'plagiarism_data'

# """
# DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
# """

# make_csv(train_x, train_y, filename='train.csv', data_dir=data_dir)
# make_csv(test_x, test_y, filename='test.csv', data_dir=data_dir)