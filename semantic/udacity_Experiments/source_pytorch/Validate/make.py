import os
import csv
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer

def dataLoader(folderName):
    fileNames = []
    
    for fileName in os.listdir(folderName):
        fileNames.append(fileName)
    
    with open('data/file_information.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                        lineterminator='\n')
    
        filewriter.writerow(['File','Source'])
        
        for fileName1 in fileNames :
            if fileName1 == 'file_information.csv':
                continue
            for fileName2 in fileNames :
                if fileName2 == 'file_information.csv':
                    continue  
                if fileName1 != fileName2 :
                    filewriter.writerow([fileName1, fileName2])

def process_file(file):
    all_text = file.read().lower()
    all_text = re.sub(r"[^a-zA-Z0-9]", " ", all_text)
    all_text = re.sub(r"\t", " ", all_text)
    all_text = re.sub(r"\n", " ", all_text)
    all_text = re.sub("  ", " ", all_text)
    all_text = re.sub("   ", " ", all_text)
    return all_text

def create_text_column(df, file_directory='data/'):
    text_df = df.copy()
    text = []
    for row_i in df.index:
        filename = df.iloc[row_i]['File']
        #print(filename)
        file_path = file_directory + filename
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            file_text = process_file(file)
            text.append(file_text)

    text_df['Text'] = text  
    return text_df

def calculate_containment(df, n, answer_filename):
    answer_df = df.query('File == @answer_filename')
    a_text = answer_df.iloc[0].at['Text']
    source_filename = answer_df.iloc[0].at['Source']
    source_df = df.query('File == @source_filename')
    s_text = source_df.iloc[0].at['Text']

    counts = CountVectorizer(analyzer='word', ngram_range=(n,n))
    ngrams = counts.fit_transform([a_text, s_text])
    ngram_array = ngrams.toarray()

    intersection = [min(a, s) for a, s in zip(*ngram_array)]
    c_value = sum(intersection) / sum(ngram_array[0])

    return c_value

def lcs_norm_word(answer_text, source_text):

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

def create_containment_features(df, n, column_name=None):
    containment_values = []
    
    if(column_name==None):
        column_name = 'c_'+str(n)
    
    for i in df.index:
        file = df.loc[i, 'File']

        c = calculate_containment(df, n, file)
        containment_values.append(c)
    
    print(str(n)+'-gram containment features created!')
    return containment_values

def create_lcs_features(df, column_name='lcs_word'):
    lcs_values = []
    
    for i in df.index:
        answer_text = df.loc[i, 'Text']
        answer_filename = df.loc[i, 'File'] 
        source_filename = df.loc[i, 'Source']
        # source_filename = "source" + answer_filename[6:]     
        source_df = df.query('File == @source_filename')
        source_text = source_df.iloc[0].at['Text']

        # calculate lcs
        lcs = lcs_norm_word(answer_text, source_text)
        lcs_values.append(lcs)

    print('LCS features created!')
    return lcs_values

def train_test_data(complete_df, features_df, selected_features):
    train_test_df = complete_df.join(features_df[selected_features])
    train_x = train_test_df[selected_features]
    return (train_x.values)

def make_csv(x, filename, data_dir):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    file_path = str(data_dir)+'/'+str(filename)
    
    y=[]
    for item in x : 
        y.append(1)

    df = pd.DataFrame([(label, *cols) for (label, cols) in zip(y, x)])
    df.dropna(axis=0)

    df.to_csv(file_path, header=False, index=False)
    print('Path created: '+file_path)

if __name__ == '__main__':
    folderName = "data"
    dataLoader(folderName)
    
    csv_file = 'data/file_information.csv'
    plagiarism_df = pd.read_csv(csv_file)
    text_df = create_text_column(plagiarism_df)

    ngram_range = [1,2]
    features_list = []
    all_features = np.zeros((len(ngram_range)+1, len(text_df)))

    i=0
    for n in ngram_range:
        column_name = 'c_'+str(n)
        features_list.append(column_name)

        all_features[i]=np.squeeze(create_containment_features(text_df, n))
        i+=1

    features_list.append('lcs_word')
    all_features[i]= np.squeeze(create_lcs_features(text_df))
    features_df = pd.DataFrame(np.transpose(all_features), columns=features_list)

    # print('Features: ', features_list)

    test_selection = list(features_df)[:3] # first couple columns as a test
    print(test_selection)
    (train_x) = train_test_data(text_df, features_df, test_selection)

    data_dir = 'plagiarism_data'

    make_csv(train_x, filename='train.csv', data_dir=data_dir)